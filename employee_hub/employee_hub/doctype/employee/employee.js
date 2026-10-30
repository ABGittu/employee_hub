// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
    setup(frm) {
        // Set dynamic filter on designation based on the currently selected department
        frm.set_query("designation", function () {
            return {
                filters: {
                    department: frm.doc.department || "",
                    is_active: 1
                }
            };
        });

        // Filter active departments only
        frm.set_query("department", function () {
            return {
                filters: {
                    is_active: 1
                }
            };
        });

        // Filter reporting manager to avoid selecting oneself
        frm.set_query("reporting_manager", function () {
            return {
                filters: {
                    name: ["!=", frm.doc.name || ""],
                    employee_status: "Active"
                }
            };
        });
    },

    refresh(frm) {
        // 1. Setup Status Dashboard Indicator
        set_status_indicator(frm);

        if (!frm.is_new()) {
            // 2. Custom Button: "Create Leave Request"
            frm.add_custom_button(__("Create Leave Request"), function () {
                frappe.route_options = {
                    employee: frm.doc.name
                };
                frappe.new_doc("Leave Request");
            }, __("Actions"));

            // 3. Custom Button: "View Skills Summary" Dialog
            frm.add_custom_button(__("View Skills Summary"), function () {
                show_skills_summary_dialog(frm);
            }, __("Actions"));
        }
    },

    first_name(frm) {
        update_full_name_preview(frm);
    },

    last_name(frm) {
        update_full_name_preview(frm);
    },

    department(frm) {
        // On department change, clear designation to prevent mismatched selections
        if (frm.doc.designation) {
            frm.set_value("designation", null);
        }
    }
});

/**
 * Updates full_name client-side instantly as user types first_name or last_name
 */
function update_full_name_preview(frm) {
    const first = (frm.doc.first_name || "").trim();
    const last = (frm.doc.last_name || "").trim();
    const full = [first, last].filter(Boolean).join(" ");
    frm.set_value("full_name", full);
}

/**
 * Renders dashboard indicator badge according to employee_status:
 * Green = Active, Orange = On Leave, Red = Terminated, Gray = Inactive
 */
function set_status_indicator(frm) {
    if (frm.is_new() || !frm.doc.employee_status) return;

    const status_color_map = {
        "Active": "green",
        "On Leave": "orange",
        "Terminated": "red",
        "Inactive": "gray"
    };

    const color = status_color_map[frm.doc.employee_status] || "blue";

    // Set page title indicator
    frm.page.set_indicator(frm.doc.employee_status, color);

    // Set headline alert banner in dashboard
    frm.dashboard.clear_headline();
    frm.dashboard.set_headline_alert(
        `<div class="employee-status-headline">
            <strong>${__("Status")}:</strong>
            <span class="indicator-pill ${frm.doc.employee_status.toLowerCase().replace(" ", "-")}">${__(frm.doc.employee_status)}</span>
            <span class="text-muted" style="margin-left: 10px;">| ${__("Leave Balance")}: <strong>${frm.doc.annual_leave_balance || 0} ${__("days")}</strong></span>
        </div>`,
        color
    );
}

/**
 * Opens a modal dialog displaying a tabular summary of employee's skills
 */
function show_skills_summary_dialog(frm) {
    const skills = frm.doc.skills || [];

    let rows_html = "";
    if (skills.length === 0) {
        rows_html = `<tr><td colspan="4" class="text-center text-muted" style="padding: 16px;">${__("No skills registered for this employee.")}</td></tr>`;
    } else {
        rows_html = skills.map((row, idx) => `
            <tr>
                <td>${idx + 1}</td>
                <td><strong>${frappe.utils.escape_html(row.skill || "")}</strong></td>
                <td>
                    <span class="badge" style="background: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 4px;">
                        ${frappe.utils.escape_html(row.proficiency || "")}
                    </span>
                </td>
                <td>${row.years_of_experience ? row.years_of_experience + " " + __("years") : "-"}</td>
            </tr>
        `).join("");
    }

    const content = `
        <div style="margin-bottom: 15px;">
            <p><strong>${__("Employee")}:</strong> ${frappe.utils.escape_html(frm.doc.full_name)} (${frm.doc.name})</p>
            <p><strong>${__("Designation")}:</strong> ${frappe.utils.escape_html(frm.doc.designation || "-")} | <strong>${__("Department")}:</strong> ${frappe.utils.escape_html(frm.doc.department || "-")}</p>
        </div>
        <table class="table table-bordered table-hover" style="font-size: 13px;">
            <thead class="thead-light">
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>${__("Skill")}</th>
                    <th>${__("Proficiency")}</th>
                    <th>${__("Experience")}</th>
                </tr>
            </thead>
            <tbody>
                ${rows_html}
            </tbody>
        </table>
    `;

    const dialog = new frappe.ui.Dialog({
        title: __("Skills Summary - {0}", [frm.doc.full_name]),
        size: "large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "skills_html",
                options: content
            }
        ],
        primary_action_label: __("Close"),
        primary_action() {
            dialog.hide();
        }
    });

    dialog.show();
}
