# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import os
import frappe
from frappe.utils import getdate, now_datetime


def seed_all_sample_data():
    """
    Utility command to seed all required sample records, test users,
    print format synchronization, and dashboard metrics.
    Can be run via:
        bench --site <site_name> execute employee_hub.setup_sample_data.seed_all_sample_data
    """
    frappe.set_user("Administrator")
    print("--- Seeding Employee Hub Sample Data ---")

    seed_leave_configuration()
    seed_departments()
    seed_designations()
    seed_skills()
    seed_employees()
    seed_leave_requests()
    sync_print_format()
    create_test_users()
    setup_dashboard_and_workspace()

    frappe.db.commit()
    print("--- All sample data, test users, and dashboards successfully configured! ---")


def seed_leave_configuration():
    """Initializes global Leave Configuration settings."""
    config = frappe.get_single("Leave Configuration")
    config.default_annual_balance = 24
    config.max_casual_leave = 12
    config.max_sick_leave = 6
    config.max_earned_leave = 15
    config.allow_backdated_leave = 0
    config.max_leave_days_per_request = 15
    config.save(ignore_permissions=True)
    print(" [✓] Leave Configuration updated.")


def seed_departments():
    """Seeds at least 5 standard departments."""
    departments = [
        {"department_name": "Engineering", "department_head": "Rajesh Kumar", "is_active": 1},
        {"department_name": "Human Resources", "department_head": "Priya Shah", "is_active": 1},
        {"department_name": "Marketing", "department_head": "Amit Desai", "is_active": 1},
        {"department_name": "Finance", "department_head": "Neha Patel", "is_active": 1},
        {"department_name": "Operations", "department_head": "Vikram Singh", "is_active": 1},
    ]

    for d in departments:
        if not frappe.db.exists("Department", d["department_name"]):
            doc = frappe.get_doc({"doctype": "Department", **d})
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Department: {d['department_name']}")
        else:
            print(f" [-] Department already exists: {d['department_name']}")


def seed_designations():
    """Seeds at least 6 standard designations."""
    designations = [
        {"designation_name": "Junior Developer", "department": "Engineering", "level": "Junior"},
        {"designation_name": "Senior Developer", "department": "Engineering", "level": "Senior"},
        {"designation_name": "Tech Lead", "department": "Engineering", "level": "Lead"},
        {"designation_name": "HR Executive", "department": "Human Resources", "level": "Mid"},
        {"designation_name": "HR Manager", "department": "Human Resources", "level": "Manager"},
        {"designation_name": "Marketing Analyst", "department": "Marketing", "level": "Mid"},
        {"designation_name": "Finance Manager", "department": "Finance", "level": "Manager"},
    ]

    for des in designations:
        if not frappe.db.exists("Designation", des["designation_name"]):
            doc = frappe.get_doc({"doctype": "Designation", "is_active": 1, **des})
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Designation: {des['designation_name']}")
        else:
            print(f" [-] Designation already exists: {des['designation_name']}")


def seed_skills():
    """Seeds at least 8 standard skills."""
    skills = [
        {"skill_name": "Python", "skill_category": "Technical"},
        {"skill_name": "JavaScript", "skill_category": "Technical"},
        {"skill_name": "Frappe Framework", "skill_category": "Technical"},
        {"skill_name": "Communication", "skill_category": "Soft Skill"},
        {"skill_name": "Leadership", "skill_category": "Soft Skill"},
        {"skill_name": "Accounting", "skill_category": "Domain"},
        {"skill_name": "Git", "skill_category": "Tool"},
        {"skill_name": "SQL", "skill_category": "Technical"},
    ]

    for s in skills:
        if not frappe.db.exists("Skill", s["skill_name"]):
            doc = frappe.get_doc({"doctype": "Skill", "is_active": 1, **s})
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Skill: {s['skill_name']}")
        else:
            print(f" [-] Skill already exists: {s['skill_name']}")


def seed_employees():
    """Seeds at least 4 standard employees with child table skills."""
    employees = [
        {
            "first_name": "Karan",
            "last_name": "Mistry",
            "employee_email": "karan@sanskar.io",
            "phone": "+91 98765 43210",
            "department": "Engineering",
            "designation": "Tech Lead",
            "date_of_joining": "2022-01-15",
            "date_of_birth": "1994-06-20",
            "blood_group": "O+",
            "skills": [
                {"skill": "Python", "proficiency": "Expert", "years_of_experience": 5.0},
                {"skill": "Frappe Framework", "proficiency": "Expert", "years_of_experience": 4.0},
                {"skill": "JavaScript", "proficiency": "Advanced", "years_of_experience": 4.0},
                {"skill": "Leadership", "proficiency": "Advanced", "years_of_experience": 3.0},
            ],
        },
        {
            "first_name": "Ravi",
            "last_name": "Patel",
            "employee_email": "ravi@sanskar.io",
            "phone": "+91 98765 43211",
            "department": "Engineering",
            "designation": "Senior Developer",
            "date_of_joining": "2023-06-01",
            "date_of_birth": "1997-03-14",
            "blood_group": "B+",
            "skills": [
                {"skill": "Python", "proficiency": "Advanced", "years_of_experience": 3.0},
                {"skill": "SQL", "proficiency": "Advanced", "years_of_experience": 3.0},
                {"skill": "Git", "proficiency": "Intermediate", "years_of_experience": 2.5},
            ],
        },
        {
            "first_name": "Priya",
            "last_name": "Shah",
            "employee_email": "priya@sanskar.io",
            "phone": "+91 98765 43212",
            "department": "Human Resources",
            "designation": "HR Manager",
            "date_of_joining": "2021-03-10",
            "date_of_birth": "1992-11-05",
            "blood_group": "A+",
            "skills": [
                {"skill": "Communication", "proficiency": "Expert", "years_of_experience": 6.0},
                {"skill": "Leadership", "proficiency": "Expert", "years_of_experience": 5.0},
            ],
        },
        {
            "first_name": "Amit",
            "last_name": "Desai",
            "employee_email": "amit@sanskar.io",
            "phone": "+91 98765 43213",
            "department": "Marketing",
            "designation": "Marketing Analyst",
            "date_of_joining": "2024-01-20",
            "date_of_birth": "1999-08-25",
            "blood_group": "AB+",
            "skills": [
                {"skill": "Communication", "proficiency": "Advanced", "years_of_experience": 2.0},
                {"skill": "SQL", "proficiency": "Intermediate", "years_of_experience": 1.5},
            ],
        },
    ]

    for emp_data in employees:
        existing = frappe.db.get_value("Employee", {"employee_email": emp_data["employee_email"]}, "name")
        if not existing:
            doc = frappe.get_doc({
                "doctype": "Employee",
                "first_name": emp_data["first_name"],
                "last_name": emp_data["last_name"],
                "employee_email": emp_data["employee_email"],
                "phone": emp_data.get("phone"),
                "department": emp_data["department"],
                "designation": emp_data["designation"],
                "date_of_joining": emp_data["date_of_joining"],
                "date_of_birth": emp_data["date_of_birth"],
                "annual_leave_balance": 24,
                "employee_status": "Active",
                "blood_group": emp_data.get("blood_group"),
            })
            for s in emp_data.get("skills", []):
                doc.append("skills", s)
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Employee: {doc.full_name} ({doc.name})")
        else:
            print(f" [-] Employee already exists for email: {emp_data['employee_email']}")


def seed_leave_requests():
    """Seeds at least 3 standard leave requests."""
    # Temporarily allow backdated leave so historical assessment records can be inserted
    config = frappe.get_single("Leave Configuration")
    orig_allow_backdated = config.allow_backdated_leave
    config.allow_backdated_leave = 1
    config.save(ignore_permissions=True)

    try:
        karan = frappe.db.get_value("Employee", {"employee_email": "karan@sanskar.io"}, "name")
        ravi = frappe.db.get_value("Employee", {"employee_email": "ravi@sanskar.io"}, "name")
        amit = frappe.db.get_value("Employee", {"employee_email": "amit@sanskar.io"}, "name")

        requests = []
        if ravi:
            requests.append({
                "employee": ravi,
                "from_date": "2026-04-20",
                "to_date": "2026-04-22",
                "leave_type": "Casual Leave",
                "reason": "Family function",
            })
        if amit:
            requests.append({
                "employee": amit,
                "from_date": "2026-04-25",
                "to_date": "2026-04-25",
                "leave_type": "Sick Leave",
                "reason": "Doctor appointment",
            })
        if karan:
            requests.append({
                "employee": karan,
                "from_date": "2026-05-01",
                "to_date": "2026-05-05",
                "leave_type": "Earned Leave",
                "reason": "Vacation",
            })

        for req in requests:
            existing = frappe.db.get_value(
                "Leave Request",
                {"employee": req["employee"], "from_date": req["from_date"], "to_date": req["to_date"]},
                "name",
            )
            if not existing:
                doc = frappe.get_doc({
                    "doctype": "Leave Request",
                    "employee": req["employee"],
                    "from_date": req["from_date"],
                    "to_date": req["to_date"],
                    "leave_type": req["leave_type"],
                    "reason": req["reason"],
                })
                doc.insert(ignore_permissions=True)
                doc.submit()
                print(f" [✓] Created & Submitted Leave Request: {doc.name} for {doc.employee_name}")
            else:
                print(f" [-] Leave Request already exists: {existing}")
    finally:
        # Restore configuration to original policy
        config.allow_backdated_leave = orig_allow_backdated
        config.save(ignore_permissions=True)


def sync_print_format():
    """Ensures Employee ID Card has its Jinja HTML template saved in the database."""
    if frappe.db.exists("Print Format", "Employee ID Card"):
        pf = frappe.get_doc("Print Format", "Employee ID Card")
        path = frappe.get_app_path(
            "employee_hub",
            "employee_hub",
            "print_format",
            "employee_id_card",
            "employee_id_card.html",
        )
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                pf.html = f.read()
        pf.standard = "Yes"
        pf.custom_format = 1
        pf.print_format_type = "Jinja"
        pf.save(ignore_permissions=True)
        print(" [✓] Employee ID Card Print Format synced with database.")


def create_test_users():
    """Creates HR Admin and Employee test users for role permission evaluation."""
    from frappe.utils.password import update_password

    # 1. HR Admin user
    if not frappe.db.exists("User", "hr_admin@sanskar.io"):
        hr_user = frappe.get_doc({
            "doctype": "User",
            "email": "hr_admin@sanskar.io",
            "first_name": "HR",
            "last_name": "Admin",
            "send_welcome_email": 0,
            "roles": [{"role": "HR Admin"}, {"role": "Desk User"}],
        })
        hr_user.insert(ignore_permissions=True)
        update_password("hr_admin@sanskar.io", "admin123")
        print(" [✓] Created User: hr_admin@sanskar.io (Password: admin123, Role: HR Admin)")
    else:
        print(" [-] User hr_admin@sanskar.io already exists.")

    # 2. Employee user (Karan Mistry)
    if not frappe.db.exists("User", "karan@sanskar.io"):
        emp_user = frappe.get_doc({
            "doctype": "User",
            "email": "karan@sanskar.io",
            "first_name": "Karan",
            "last_name": "Mistry",
            "send_welcome_email": 0,
            "roles": [{"role": "Employee"}, {"role": "Desk User"}],
        })
        emp_user.insert(ignore_permissions=True)
        update_password("karan@sanskar.io", "employee123")
        print(" [✓] Created User: karan@sanskar.io (Password: employee123, Role: Employee)")
    else:
        print(" [-] User karan@sanskar.io already exists.")

    # 3. User Permission: restrict Karan to his own Employee record
    karan_emp = frappe.db.get_value("Employee", {"employee_email": "karan@sanskar.io"}, "name")
    if karan_emp and not frappe.db.exists(
        "User Permission", {"user": "karan@sanskar.io", "allow": "Employee"}
    ):
        up = frappe.get_doc({
            "doctype": "User Permission",
            "user": "karan@sanskar.io",
            "allow": "Employee",
            "for_value": karan_emp,
        })
        up.insert(ignore_permissions=True)
        print(f" [✓] Created User Permission: karan@sanskar.io restricted to Employee {karan_emp}")


def setup_dashboard_and_workspace():
    """Sets up Number Cards, Dashboard Charts, and the Workspace."""
    print("--- Setting up Dashboard & Workspace ---")

    # 1. Number Cards
    cards = [
        {
            "name": "Total Employees",
            "label": "Total Employees",
            "function": "Count",
            "document_type": "Employee",
            "color": "#3b82f6",
        },
        {
            "name": "Active Employees",
            "label": "Active Employees",
            "function": "Count",
            "document_type": "Employee",
            "filters_json": '[["Employee","employee_status","=","Active"]]',
            "color": "#10b981",
        },
        {
            "name": "Pending Leave Requests",
            "label": "Pending Leave Requests",
            "function": "Count",
            "document_type": "Leave Request",
            "filters_json": '[["Leave Request","approval_status","=","Pending"]]',
            "color": "#f59e0b",
        },
        {
            "name": "Employees On Leave",
            "label": "Employees On Leave",
            "function": "Count",
            "document_type": "Employee",
            "filters_json": '[["Employee","employee_status","=","On Leave"]]',
            "color": "#ec4899",
        },
    ]

    for c in cards:
        if not frappe.db.exists("Number Card", c["name"]):
            doc = frappe.get_doc({
                "doctype": "Number Card",
                "is_standard": 1,
                "module": "Employee Hub",
                **c,
            })
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Number Card: {c['name']}")
        else:
            print(f" [-] Number Card already exists: {c['name']}")

    # 2. Dashboard Charts
    charts = [
        {
            "chart_name": "Department Wise Employee Strength",
            "chart_type": "Group By",
            "document_type": "Employee",
            "group_by_based_on": "department",
            "group_by_type": "Count",
            "type": "Bar",
            "is_standard": 1,
            "module": "Employee Hub",
            "color": "#3b82f6",
            "filters_json": "[]",
            "timespan": "Last Year",
            "custom_options": '{"tooltipOptions": {"formatTooltipY": "d => d"}, "axisOptions": {"shortenYAxisNumbers": 0}}',
        },
        {
            "chart_name": "Employees by Department",
            "chart_type": "Group By",
            "document_type": "Employee",
            "group_by_based_on": "department",
            "group_by_type": "Count",
            "type": "Donut",
            "is_standard": 1,
            "module": "Employee Hub",
            "color": "#3b82f6",
            "filters_json": "[]",
            "timespan": "Last Year",
            "custom_options": '{"tooltipOptions": {"formatTooltipY": "d => d"}}',
        },
        {
            "chart_name": "Leave Requests by Status",
            "chart_type": "Group By",
            "document_type": "Leave Request",
            "group_by_based_on": "approval_status",
            "group_by_type": "Count",
            "type": "Donut",
            "is_standard": 1,
            "module": "Employee Hub",
            "color": "#10b981",
            "filters_json": "[]",
            "timespan": "Last Year",
            "custom_options": '{"tooltipOptions": {"formatTooltipY": "d => d"}}',
        },
    ]

    for ch in charts:
        if not frappe.db.exists("Dashboard Chart", ch["chart_name"]):
            doc = frappe.get_doc({
                "doctype": "Dashboard Chart",
                "is_standard": 1,
                "module": "Employee Hub",
                **ch,
            })
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Dashboard Chart: {ch['chart_name']}")
        else:
            doc = frappe.get_doc("Dashboard Chart", ch["chart_name"])
            doc.type = ch["type"]
            doc.custom_options = ch.get("custom_options")
            doc.save(ignore_permissions=True)
            print(f" [✓] Updated Dashboard Chart: {ch['chart_name']}")

    # 3. Ensure Workspace is loaded in database
    import json
    ws_path = frappe.get_app_path(
        "employee_hub", "employee_hub", "workspace", "employee_hub", "employee_hub.json"
    )
    if os.path.exists(ws_path):
        with open(ws_path, "r", encoding="utf-8") as f:
            ws_data = json.load(f)

        # Always force type field (required in Frappe v16)
        ws_data["type"] = "Workspace"

        if not frappe.db.exists("Workspace", "Employee Hub"):
            ws_doc = frappe.get_doc(ws_data)
            ws_doc.insert(ignore_permissions=True)
            print(" [✓] Created Workspace: Employee Hub")
        else:
            # Load the existing doc and update ALL fields via ORM (not db.set_value)
            # so that child tables (charts, number_cards, shortcuts, links) are
            # fully replaced — not patched one-by-one.
            ws_doc = frappe.get_doc("Workspace", "Employee Hub")

            # Scalar fields
            ws_doc.content       = ws_data.get("content", "[]")
            ws_doc.type          = "Workspace"
            ws_doc.is_hidden     = 0
            ws_doc.public        = 1
            ws_doc.icon          = ws_data.get("icon", "users")
            ws_doc.module        = ws_data.get("module", "Employee Hub")
            ws_doc.title         = ws_data.get("title", "Employee Hub")
            ws_doc.label         = ws_data.get("label", "Employee Hub")
            ws_doc.sequence_id   = ws_data.get("sequence_id", 1.0)
            ws_doc.indicator_color = ws_data.get("indicator_color", "blue")

            # Replace child tables via set() + append() to avoid stale rows
            ws_doc.set("charts", [])
            for ch in ws_data.get("charts", []):
                ws_doc.append("charts", {
                    "chart_name": ch.get("chart_name"),
                    "label":      ch.get("label") or ch.get("chart_name"),
                })

            ws_doc.set("number_cards", [])
            for nc in ws_data.get("number_cards", []):
                ws_doc.append("number_cards", {
                    "number_card_name": nc.get("number_card_name"),
                    "label":            nc.get("label") or nc.get("number_card_name"),
                })

            ws_doc.set("shortcuts", [])
            for sc in ws_data.get("shortcuts", []):
                ws_doc.append("shortcuts", {
                    "label":    sc.get("label"),
                    "link_to":  sc.get("link_to"),
                    "type":     sc.get("type"),
                    "color":    sc.get("color"),
                    "doc_view": sc.get("doc_view", ""),
                })

            ws_doc.set("links", [])
            for lk in ws_data.get("links", []):
                ws_doc.append("links", {
                    "label":          lk.get("label"),
                    "link_to":        lk.get("link_to"),
                    "link_type":      lk.get("link_type"),
                    "type":           lk.get("type"),
                    "is_query_report": lk.get("is_query_report", 0),
                    "hidden":         lk.get("hidden", 0),
                    "onboard":        lk.get("onboard", 0),
                })

            ws_doc.save(ignore_permissions=True)

            # Clear any user-specific workspace overrides so the public one is served
            frappe.db.delete("Workspace", {"name": ["like", "%Employee Hub%"], "for_user": ["!=", ""]})
            print(" [✓] Updated Workspace: Employee Hub (charts, cards, shortcuts fully reloaded).")

    # 4. Standard Dashboard document (viewable at /app/dashboard-view/Employee Hub Dashboard)
    if not frappe.db.exists("Dashboard", "Employee Hub Dashboard"):
        dash = frappe.get_doc({
            "doctype": "Dashboard",
            "dashboard_name": "Employee Hub Dashboard",
            "module": "Employee Hub",
            "is_standard": 1,
            "charts": [
                {"chart": "Department Wise Employee Strength", "width": "Full"},
                {"chart": "Employees by Department", "width": "Half"},
                {"chart": "Leave Requests by Status", "width": "Half"},
            ],
            "cards": [
                {"card": "Total Employees"},
                {"card": "Active Employees"},
                {"card": "Pending Leave Requests"},
                {"card": "Employees On Leave"},
            ],
        })
        dash.insert(ignore_permissions=True)
        print(" [✓] Created Dashboard: Employee Hub Dashboard")
    else:
        dash = frappe.get_doc("Dashboard", "Employee Hub Dashboard")
        dash.set("charts", [])
        for c in [
            {"chart": "Department Wise Employee Strength", "width": "Full"},
            {"chart": "Employees by Department", "width": "Half"},
            {"chart": "Leave Requests by Status", "width": "Half"},
        ]:
            dash.append("charts", c)
        dash.save(ignore_permissions=True)
        print(" [✓] Updated Dashboard: Employee Hub Dashboard")
