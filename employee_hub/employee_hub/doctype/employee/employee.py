# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
    add_years,
    getdate,
    today,
    validate_email_address,
)


def set_full_name(doc, method=None):
    """
    Standalone function hooked via hooks.py doc_events:
    Ensures employee full_name is correctly populated before saving.
    """
    first = (doc.first_name or "").strip()
    last = (doc.last_name or "").strip()
    if first and last:
        doc.full_name = f"{first} {last}"
    elif first:
        doc.full_name = first
    elif last:
        doc.full_name = last


class Employee(Document):
    """
    Employee DocType Controller.
    Manages employee profiles, employment details, skill assignments,
    and leave balances.
    """

    def before_save(self):
        """
        Executed right before saving the document to the database.
        Used for computing derived fields like full_name.
        """
        set_full_name(self)

    def validate(self):
        """
        Executed during the validation lifecycle before insertion or updating.
        Enforces business rules and constraints:
        1. Generates full_name for early validation availability.
        2. Validates email format.
        3. Validates employee is at least 18 years old.
        4. Validates date of joining is not in the future.
        5. Validates date of joining is strictly after date of birth.
        """
        set_full_name(self)
        self.validate_email()
        self.validate_dates()

    def validate_email(self):
        """Validate employee email address format."""
        if self.employee_email:
            self.employee_email = self.employee_email.strip().lower()
            validate_email_address(self.employee_email, throw=True)

    def validate_dates(self):
        """Validate date_of_birth and date_of_joining constraints."""
        if not self.date_of_birth:
            frappe.throw(_("Date of Birth is mandatory."))

        if not self.date_of_joining:
            frappe.throw(_("Date of Joining is mandatory."))

        dob = getdate(self.date_of_birth)
        doj = getdate(self.date_of_joining)
        today_date = getdate(today())

        # Rule 1: Validate date_of_birth is at least 18 years before today
        eighteen_years_ago = add_years(today_date, -18)
        if dob > eighteen_years_ago:
            frappe.throw(
                _(
                    "Employee must be at least 18 years old. "
                    "Date of Birth ({0}) cannot be after {1}."
                ).format(dob, eighteen_years_ago)
            )

        # Rule 2: Validate date_of_joining is not in the future
        if doj > today_date:
            frappe.throw(
                _("Date of Joining ({0}) cannot be in the future (today is {1}).").format(
                    doj, today_date
                )
            )

        # Rule 3: Validate date_of_joining > date_of_birth
        if doj <= dob:
            frappe.throw(
                _(
                    "Date of Joining ({0}) must be strictly after Date of Birth ({1})."
                ).format(doj, dob)
            )
