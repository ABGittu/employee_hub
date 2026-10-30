# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
    date_diff,
    getdate,
    now_datetime,
    today,
)


@frappe.whitelist()
def get_employee_leave_info(employee):
    """
    Whitelisted API for client script to fetch employee's current leave balance
    and active leave configuration limits.
    """
    if not employee:
        return {}

    emp = frappe.db.get_value(
        "Employee",
        employee,
        ["full_name", "department", "annual_leave_balance", "employee_status"],
        as_dict=True,
    )
    config = frappe.get_single("Leave Configuration")

    return {
        "employee_name": emp.full_name if emp else "",
        "department": emp.department if emp else "",
        "annual_leave_balance": emp.annual_leave_balance if emp else 0,
        "employee_status": emp.employee_status if emp else "",
        "max_leave_days_per_request": config.max_leave_days_per_request or 15,
        "allow_backdated_leave": bool(config.allow_backdated_leave),
    }


class LeaveRequest(Document):
    """
    Leave Request DocType Controller (Submittable).
    Handles employee leave application, validations against policies,
    overlap checks, and leave balance deductions/restorations.
    """

    def validate(self):
        """
        Validate leave request prior to saving or submitting.
        Calculates total days and verifies all business constraints.
        """
        self.calculate_total_days()
        self.validate_employee_own_record()
        self.validate_rejected_state()
        self.validate_with_leave_configuration()
        self.validate_leave_balance()
        self.validate_no_overlapping_approved_leaves()

    def validate_employee_own_record(self):
        """
        Enforce own-record restriction for users with Employee role
        who do not possess administrative roles, ensuring no cross-employee
        leave requests can be lodged even in the absence of seed User Permissions.
        """
        if frappe.session.user == "Administrator":
            return

        roles = set(frappe.get_roles(frappe.session.user))
        if "Employee" in roles and not ({"HR Admin", "System Manager"} & roles):
            user_emp = frappe.db.get_value(
                "Employee", {"employee_email": frappe.session.user}, "name"
            )
            if user_emp and self.employee != user_emp:
                frappe.throw(
                    _(
                        "You are only allowed to submit leave requests for your own Employee record ({0})."
                    ).format(user_emp)
                )

    def validate_rejected_state(self):
        """
        Enforce rejection integrity:
        1. When in Rejected state, rejection_reason is strictly mandatory.
        2. Prevent direct edits while remaining in Rejected state without resubmission.
        """
        if self.approval_status == "Rejected":
            if not (self.rejection_reason or "").strip():
                frappe.throw(
                    _("Rejection Reason is mandatory when rejecting a leave request.")
                )

            # Prevent saving manual modifications while still in Rejected state
            if not self.is_new() and not getattr(self.flags, "in_workflow_transition", False):
                if self._doc_before_save and self._doc_before_save.approval_status == "Rejected":
                    frappe.throw(
                        _(
                            "Rejected leave requests cannot be edited directly. "
                            "Please click 'Resubmit' to reopen the request."
                        )
                    )

    def calculate_total_days(self):
        """
        Calculate total days requested inclusive of start and end dates.
        total_days = date_diff(to_date, from_date) + 1
        """
        if not self.from_date or not self.to_date:
            frappe.throw(_("Both From Date and To Date are mandatory."))

        from_d = getdate(self.from_date)
        to_d = getdate(self.to_date)

        if to_d < from_d:
            frappe.throw(_("To Date ({0}) cannot be before From Date ({1}).").format(to_d, from_d))

        days = date_diff(to_d, from_d) + 1
        self.total_days = float(days)

    def validate_with_leave_configuration(self):
        """
        Validates the request against rules defined in Leave Configuration Single DocType:
        1. Backdated leaves check.
        2. Maximum allowed days per single request.
        3. Leave type specific thresholds.
        """
        config = frappe.get_single("Leave Configuration")
        from_d = getdate(self.from_date)
        today_date = getdate(today())

        # Check backdated leave restriction
        if not config.allow_backdated_leave and from_d < today_date:
            frappe.throw(
                _(
                    "From Date ({0}) is in the past. Backdated leave requests are disallowed "
                    "per company Leave Configuration."
                ).format(from_d)
            )

        # Check maximum days per request
        max_days = config.max_leave_days_per_request or 15
        if self.total_days > max_days:
            frappe.throw(
                _(
                    "Requested leave of {0} days exceeds the maximum allowed limit of {1} days "
                    "per request configured in Leave Configuration."
                ).format(self.total_days, max_days)
            )

        # Check type-specific thresholds
        if self.leave_type == "Casual Leave" and config.max_casual_leave:
            if self.total_days > config.max_casual_leave:
                frappe.throw(
                    _("Casual Leave request ({0} days) exceeds the limit of {1} days.").format(
                        self.total_days, config.max_casual_leave
                    )
                )
        elif self.leave_type == "Sick Leave" and config.max_sick_leave:
            if self.total_days > config.max_sick_leave:
                frappe.throw(
                    _("Sick Leave request ({0} days) exceeds the limit of {1} days.").format(
                        self.total_days, config.max_sick_leave
                    )
                )
        elif self.leave_type == "Earned Leave" and config.max_earned_leave:
            if self.total_days > config.max_earned_leave:
                frappe.throw(
                    _("Earned Leave request ({0} days) exceeds the limit of {1} days.").format(
                        self.total_days, config.max_earned_leave
                    )
                )

    def validate_leave_balance(self):
        """
        Verify that employee has adequate annual leave balance to cover total_days.
        """
        if not self.employee:
            frappe.throw(_("Employee must be selected."))

        available_balance = (
            frappe.db.get_value("Employee", self.employee, "annual_leave_balance") or 0
        )

        if self.total_days > available_balance:
            frappe.throw(
                _(
                    "Insufficient annual leave balance for employee '{0}'. "
                    "Requested: {1} days, Available Balance: {2} days."
                ).format(self.employee_name or self.employee, self.total_days, available_balance)
            )

    def validate_no_overlapping_approved_leaves(self):
        """
        Prevent duplicate or conflicting leave periods for the same employee.
        Checks for any existing submitted/approved leave overlapping the given dates.
        """
        overlapping = frappe.db.sql(
            """
            SELECT name, from_date, to_date, leave_type
            FROM `tabLeave Request`
            WHERE employee = %(employee)s
              AND name != %(current_name)s
              AND docstatus = 1
              AND approval_status = 'Approved'
              AND from_date <= %(to_date)s
              AND to_date >= %(from_date)s
            LIMIT 1
            """,
            {
                "employee": self.employee,
                "current_name": self.name or "",
                "from_date": self.from_date,
                "to_date": self.to_date,
            },
            as_dict=True,
        )

        if overlapping:
            match = overlapping[0]
            frappe.throw(
                _(
                    "Overlapping approved leave request detected! "
                    "Record '{0}' ({1}) is already approved from {2} to {3}."
                ).format(match.name, match.leave_type, match.from_date, match.to_date)
            )

    def on_submit(self):
        """
        Triggered when Leave Request is submitted (docstatus transitions 0 -> 1):
        1. Set approval_status to 'Approved'.
        2. Set approved_by to session user and approval_date to now.
        3. Deduct total_days from employee's annual_leave_balance.
        4. If leave is currently active today, set employee_status to 'On Leave'.
        """
        self.approval_status = "Approved"
        self.approved_by = frappe.session.user
        self.approval_date = now_datetime()

        self.db_set("approval_status", "Approved")
        self.db_set("approved_by", self.approved_by)
        self.db_set("approval_date", self.approval_date)

        # Update Employee Document
        emp = frappe.get_doc("Employee", self.employee)
        current_balance = emp.annual_leave_balance or 0
        emp.annual_leave_balance = max(0, current_balance - int(self.total_days))

        # Check if the employee is currently active on leave today
        today_date = getdate(today())
        if getdate(self.from_date) <= today_date <= getdate(self.to_date):
            emp.employee_status = "On Leave"

        emp.save(ignore_permissions=True)

        frappe.msgprint(
            _(
                "Leave Request approved successfully. Deducted {0} days from {1}'s balance. Remaining balance: {2} days."
            ).format(self.total_days, emp.full_name, emp.annual_leave_balance),
            alert=True,
        )

    def on_cancel(self):
        """
        Triggered when Leave Request is cancelled (docstatus transitions 1 -> 2):
        1. Set approval_status to 'Cancelled' (preserves workflow state cleanly).
        2. Restore total_days to employee's annual_leave_balance.
        3. Reset employee_status to 'Active' if it was marked 'On Leave'.
        """
        self.approval_status = "Cancelled"
        self.db_set("approval_status", "Cancelled")

        # Restore leave balance to Employee
        emp = frappe.get_doc("Employee", self.employee)
        emp.annual_leave_balance = (emp.annual_leave_balance or 0) + int(self.total_days)

        if emp.employee_status == "On Leave":
            emp.employee_status = "Active"

        emp.save(ignore_permissions=True)

        frappe.msgprint(
            _(
                "Leave Request Cancelled. Restored {0} days to {1}'s balance. Current balance: {2} days."
            ).format(self.total_days, emp.full_name, emp.annual_leave_balance),
            alert=True,
        )
