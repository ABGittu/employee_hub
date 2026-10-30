// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Request", {
    setup(frm) {
        // Filter employee to only show Active employees
        frm.set_query("employee", function () {
            return {
                filters: {
                    employee_status: "Active"
                }
            };
        });

        // Restrict employee field if logged-in user is an Employee (not HR Admin / System Manager)
        if (
            frappe.user_roles.includes("Employee") &&
            !frappe.user_roles.includes("HR Admin") &&
            !frappe.user_roles.includes("System Manager") &&
            frappe.session.user !== "Administrator"
        ) {
            if (frm.is_new()) {
                frappe.db.get_value("Employee", { employee_email: frappe.session.user }, "name")
                    .then(r => {
                        if (r && r.message && r.message.name) {
                            frm.set_value("employee", r.message.name);
                            frm.set_df_property("employee", "read_only", 1);
                        }
                    });
            } else {
                frm.set_df_property("employee", "read_only", 1);
            }
        }
    },

    refresh(frm) {
        // Update leave intro message if employee is selected
        if (frm.doc.employee) {
            update_leave_balance_intro(frm);
        }

        // Style status pill in header
        if (frm.doc.approval_status) {
            const status_colors = {
                "Pending": "orange",
                "Approved": "green",
                "Rejected": "red",
                "Cancelled": "gray"
            };
            frm.page.set_indicator(frm.doc.approval_status, status_colors[frm.doc.approval_status] || "blue");
        }

        // Prevent editing and direct saving while in Rejected state
        if (frm.doc.approval_status === "Rejected") {
            frm.disable_save();
        }
    },

    employee(frm) {
        if (frm.doc.employee) {
            update_leave_balance_intro(frm);
        } else {
            frm.set_intro("");
        }
    },

    from_date(frm) {
        calculate_total_days(frm);
    },

    to_date(frm) {
        calculate_total_days(frm);
    },

    before_workflow_action(frm) {
        return new Promise((resolve, reject) => {
            const action = frm.selected_workflow_action;

            if (action === "Approve") {
                frappe.dom.unfreeze();

                const summary_msg = `
                    <div style="font-size: 14px; line-height: 1.6;">
                        <p><strong>${__("Employee")}:</strong> ${frappe.utils.escape_html(frm.doc.employee_name || frm.doc.employee)}</p>
                        <p><strong>${__("Leave Type")}:</strong> ${frappe.utils.escape_html(frm.doc.leave_type)}</p>
                        <p><strong>${__("Duration")}:</strong> ${frm.doc.from_date} ${__("to")} ${frm.doc.to_date} (<strong>${frm.doc.total_days} ${__("days")}</strong>)</p>
                        <p><strong>${__("Reason")}:</strong> ${frappe.utils.escape_html(frm.doc.reason || "")}</p>
                        <hr/>
                        <p class="text-warning"><strong>${__("Approving this request will automatically deduct {0} days from the employee's balance.", [frm.doc.total_days])}</strong></p>
                    </div>
                `;

                frappe.confirm(
                    summary_msg,
                    () => {
                        resolve();
                    },
                    () => {
                        frappe.dom.unfreeze();
                        frappe.show_alert({
                            message: __("Approval cancelled by user"),
                            indicator: "info"
                        });
                        reject();
                    }
                );
            } else if (action === "Reject") {
                frappe.dom.unfreeze();

                let prompt_submitted = false;
                const d = frappe.prompt(
                    [
                        {
                            fieldname: "rejection_reason",
                            fieldtype: "Small Text",
                            label: __("Rejection Reason"),
                            reqd: 1,
                            description: __("Please specify the reason for rejecting this leave request.")
                        }
                    ],
                    (values) => {
                        prompt_submitted = true;
                        frm.set_value("rejection_reason", values.rejection_reason);
                        resolve();
                    },
                    __("Reason for Rejection"),
                    __("Reject")
                );

                if (d && d.$wrapper) {
                    d.$wrapper.on("hidden.bs.modal", () => {
                        if (!prompt_submitted) {
                            frappe.dom.unfreeze();
                            frappe.show_alert({
                                message: __("Rejection cancelled by user"),
                                indicator: "info"
                            });
                            reject();
                        }
                    });
                }
            } else if (action === "Resubmit") {
                // Clear rejection reason on resubmission
                frm.set_value("rejection_reason", "");
                resolve();
            } else {
                resolve();
            }
        });
    }
});

/**
 * Calculates total_days client-side when from_date or to_date changes
 */
function calculate_total_days(frm) {
    if (frm.doc.from_date && frm.doc.to_date) {
        const from_date = frappe.datetime.str_to_obj(frm.doc.from_date);
        const to_date = frappe.datetime.str_to_obj(frm.doc.to_date);

        if (to_date < from_date) {
            frappe.msgprint({
                title: __("Validation Warning"),
                indicator: "orange",
                message: __("To Date cannot be earlier than From Date.")
            });
            frm.set_value("total_days", 0);
            return;
        }

        const diff_time = Math.abs(to_date - from_date);
        const diff_days = Math.ceil(diff_time / (1000 * 60 * 60 * 24)) + 1;
        frm.set_value("total_days", diff_days);

        // Check if total_days > max_leave_days_per_request from Leave Configuration
        frappe.db.get_single_value("Leave Configuration", "max_leave_days_per_request")
            .then(max_days => {
                if (max_days && diff_days > max_days) {
                    frappe.show_alert({
                        message: __("Warning: Requested {0} days exceeds company policy limit of {1} days per request!", [diff_days, max_days]),
                        indicator: "red"
                    }, 7);
                }
            });
    }
}

/**
 * Fetches remaining leave balance and displays it in the form header using frm.set_intro()
 */
function update_leave_balance_intro(frm) {
    frappe.call({
        method: "employee_hub.employee_hub.doctype.leave_request.leave_request.get_employee_leave_info",
        args: {
            employee: frm.doc.employee
        },
        callback: function (r) {
            if (r.message) {
                const info = r.message;
                const balance = info.annual_leave_balance ?? 0;
                const status = info.employee_status || "Active";

                const balance_color = balance > 5 ? "#03543f" : (balance > 0 ? "#9f580a" : "#9b1c1c");
                const intro_html = `
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                        <span>
                            <strong>${__("Employee")}:</strong> ${frappe.utils.escape_html(info.employee_name || frm.doc.employee)}
                            (${__("Status")}: <strong>${status}</strong>)
                        </span>
                        <span>
                            ${__("Remaining Annual Leave Balance")}:
                            <strong style="color: ${balance_color}; font-size: 14px;">${balance} ${__("days")}</strong>
                        </span>
                    </div>
                `;

                frm.set_intro(intro_html, balance > 0 ? "green" : "red");
            }
        }
    });
}
