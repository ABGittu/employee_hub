// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Configuration", {
    refresh(frm) {
        frm.set_intro(__("Configure company-wide leave limits, balances, and backdated leave policies."));
    }
});
