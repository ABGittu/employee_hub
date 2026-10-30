# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class LeaveConfiguration(Document):
    """
    Leave Configuration Single DocType Controller.
    Global policies and constraints for leave allocations and requests.
    """

    def validate(self):
        """Validate leave rules."""
        if (self.default_annual_balance or 0) < 0:
            frappe.throw(_("Default Annual Balance cannot be negative."))

        if (self.max_leave_days_per_request or 0) <= 0:
            frappe.throw(_("Max Leave Days Per Request must be at least 1 day."))
