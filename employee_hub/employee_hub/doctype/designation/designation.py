# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Designation(Document):
    """
    Designation DocType Controller.
    Manages job designations/titles categorized by organizational level and department.
    """

    def validate(self):
        """Validate designation data."""
        self.clean_fields()
        self.validate_department_active()

    def clean_fields(self):
        """Clean leading and trailing whitespace."""
        if self.designation_name:
            self.designation_name = self.designation_name.strip()

    def validate_department_active(self):
        """Ensure linked department is active if provided."""
        if self.department:
            is_active = frappe.db.get_value("Department", self.department, "is_active")
            if is_active == 0:
                frappe.throw(
                    _("Cannot assign designation to an inactive department '{0}'.").format(
                        self.department
                    )
                )
