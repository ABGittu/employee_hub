# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Skill(Document):
    """
    Skill DocType Controller.
    Manages skills categorized as Technical, Soft Skill, Domain, or Tool.
    """

    def validate(self):
        """Validate and sanitize skill record."""
        if self.skill_name:
            self.skill_name = self.skill_name.strip()
