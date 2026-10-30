# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Department(Document):
    """
    Department DocType Controller.
    Manages organizational departments within the Employee Hub System.
    """

    def validate(self):
        """Execute validations before saving."""
        self.validate_duplicate_name_case_insensitive()

    def validate_duplicate_name_case_insensitive(self):
        """
        Validate that no other department has the same name in a case-insensitive match.
        Example: If 'Engineering' exists, 'engineering' or 'ENGINEERING' should be rejected.
        """
        if not self.department_name:
            return

        cleaned_name = self.department_name.strip()
        self.department_name = cleaned_name

        existing = frappe.db.sql(
            """
            SELECT name, department_name
            FROM `tabDepartment`
            WHERE LOWER(department_name) = LOWER(%s)
              AND name != %s
            LIMIT 1
            """,
            (cleaned_name, self.name or ""),
            as_dict=True,
        )

        if existing:
            frappe.throw(
                _(
                    "A Department with name '{0}' already exists (matches '{1}' case-insensitively). "
                    "Department names must be uniquely identifiable."
                ).format(cleaned_name, existing[0].department_name)
            )
