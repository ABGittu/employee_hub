// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Department", {
    refresh(frm) {
        // Helpful tip for users about unique naming
        if (frm.is_new()) {
            frm.set_intro(__("Enter a unique department name and head of department."));
        }
    }
});
