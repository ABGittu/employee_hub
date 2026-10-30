// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.listview_settings["Employee"] = {
    add_fields: [
        "employee_status",
        "department",
        "designation",
        "date_of_joining",
        "full_name",
        "annual_leave_balance"
    ],
    get_indicator(doc) {
        if (doc.employee_status === "Active") {
            return [__("Active"), "green", "employee_status,=,Active"];
        } else if (doc.employee_status === "On Leave") {
            return [__("On Leave"), "orange", "employee_status,=,On Leave"];
        } else if (doc.employee_status === "Inactive") {
            return [__("Inactive"), "gray", "employee_status,=,Inactive"];
        } else if (doc.employee_status === "Terminated") {
            return [__("Terminated"), "red", "employee_status,=,Terminated"];
        }
        return [__("Unknown"), "gray", ""];
    }
};
