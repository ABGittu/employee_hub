// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Designation", {
    refresh(frm) {
        // Set query on department to show only active departments
        frm.set_query("department", function() {
            return {
                filters: {
                    is_active: 1
                }
            };
        });
    }
});
