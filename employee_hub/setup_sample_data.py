# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import json
import os
import frappe
from frappe.utils import add_days, getdate, today


def seed_departments():
    """Seeds at least 5 standard departments."""
    departments = [
        {"department_name": "Engineering", "is_active": 1, "description": "Software development and engineering team"},
        {"department_name": "Human Resources", "is_active": 1, "description": "Talent acquisition and people operations"},
        {"department_name": "Marketing", "is_active": 1, "description": "Brand strategy and growth marketing"},
        {"department_name": "Finance", "is_active": 1, "description": "Financial planning, accounting, and compliance"},
        {"department_name": "Operations", "is_active": 1, "description": "Business operations and infrastructure"},
    ]

    for d in departments:
        if not frappe.db.exists("Department", d["department_name"]):
            doc = frappe.get_doc({
                "doctype": "Department",
                **d
            })
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Department: {d['department_name']}")
        else:
            print(f" [-] Department already exists: {d['department_name']}")


def seed_designations():
    """Seeds at least 7 standard designations across departments."""
    designations = [
        {"designation_name": "Junior Developer", "department": "Engineering", "level": "Junior", "is_active": 1},
        {"designation_name": "Senior Developer", "department": "Engineering", "level": "Senior", "is_active": 1},
        {"designation_name": "Tech Lead", "department": "Engineering", "level": "Lead", "is_active": 1},
        {"designation_name": "HR Executive", "department": "Human Resources", "level": "Mid", "is_active": 1},
        {"designation_name": "HR Manager", "department": "Human Resources", "level": "Manager", "is_active": 1},
        {"designation_name": "Marketing Analyst", "department": "Marketing", "level": "Mid", "is_active": 1},
        {"designation_name": "Finance Manager", "department": "Finance", "level": "Manager", "is_active": 1},
        {"designation_name": "Operations Manager", "department": "Operations", "level": "Manager", "is_active": 1},
    ]

    for d in designations:
        if not frappe.db.exists("Designation", d["designation_name"]):
            doc = frappe.get_doc({
                "doctype": "Designation",
                **d
            })
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Designation: {d['designation_name']}")
        else:
            print(f" [-] Designation already exists: {d['designation_name']}")


def seed_skills():
    """Seeds at least 8 standard skills across diverse categories."""
    skills = [
        {"skill_name": "Python", "skill_category": "Technical", "is_active": 1},
        {"skill_name": "JavaScript", "skill_category": "Technical", "is_active": 1},
        {"skill_name": "Frappe Framework", "skill_category": "Technical", "is_active": 1},
        {"skill_name": "Communication", "skill_category": "Soft Skill", "is_active": 1},
        {"skill_name": "Leadership", "skill_category": "Soft Skill", "is_active": 1},
        {"skill_name": "Accounting", "skill_category": "Domain", "is_active": 1},
        {"skill_name": "Git", "skill_category": "Tool", "is_active": 1},
        {"skill_name": "SQL", "skill_category": "Technical", "is_active": 1},
    ]

    for s in skills:
        if not frappe.db.exists("Skill", s["skill_name"]):
            doc = frappe.get_doc({
                "doctype": "Skill",
                **s
            })
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Skill: {s['skill_name']}")
        else:
            print(f" [-] Skill already exists: {s['skill_name']}")


def seed_leave_configuration():
    """Configures default values on the Leave Configuration Single DocType."""
    config = frappe.get_single("Leave Configuration")
    config.default_annual_balance = 24
    config.max_leave_days_per_request = 15
    config.allow_backdated_leave = 0
    config.max_casual_leave = 5
    config.max_sick_leave = 7
    config.max_earned_leave = 15
    config.save(ignore_permissions=True)
    print(" [✓] Leave Configuration updated.")


def seed_employees():
    """Seeds at least 4 employees with skills child tables, diverse departments & designations."""
    employees_data = [
        {
            "first_name": "Karan",
            "last_name": "Mistry",
            "employee_email": "karan@sanskar.io",
            "phone": "+91 9876543210",
            "date_of_birth": "1998-05-15",
            "date_of_joining": "2022-01-15",
            "department": "Engineering",
            "designation": "Senior Developer",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "B+",
            "skills": [
                {"skill": "Python", "proficiency": "Advanced", "years_of_experience": 4},
                {"skill": "Frappe Framework", "proficiency": "Intermediate", "years_of_experience": 2},
                {"skill": "Git", "proficiency": "Advanced", "years_of_experience": 4},
            ]
        },
        {
            "first_name": "Ravi",
            "last_name": "Patel",
            "employee_email": "ravi@sanskar.io",
            "phone": "+91 9876543211",
            "date_of_birth": "1995-08-20",
            "date_of_joining": "2021-03-01",
            "department": "Engineering",
            "designation": "Tech Lead",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "O+",
            "skills": [
                {"skill": "Python", "proficiency": "Expert", "years_of_experience": 6},
                {"skill": "Leadership", "proficiency": "Advanced", "years_of_experience": 3},
                {"skill": "SQL", "proficiency": "Advanced", "years_of_experience": 5},
            ]
        },
        {
            "first_name": "Priya",
            "last_name": "Shah",
            "employee_email": "priya@sanskar.io",
            "phone": "+91 9876543212",
            "date_of_birth": "1997-11-10",
            "date_of_joining": "2023-06-15",
            "department": "Human Resources",
            "designation": "HR Manager",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "A+",
            "skills": [
                {"skill": "Communication", "proficiency": "Expert", "years_of_experience": 5},
                {"skill": "Leadership", "proficiency": "Intermediate", "years_of_experience": 2},
            ]
        },
        {
            "first_name": "Amit",
            "last_name": "Desai",
            "employee_email": "amit@sanskar.io",
            "phone": "+91 9876543213",
            "date_of_birth": "1999-02-28",
            "date_of_joining": "2024-01-10",
            "department": "Marketing",
            "designation": "Marketing Analyst",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "AB+",
            "skills": [
                {"skill": "Communication", "proficiency": "Advanced", "years_of_experience": 3},
                {"skill": "SQL", "proficiency": "Intermediate", "years_of_experience": 2},
            ]
        },
        {
            "first_name": "Neha",
            "last_name": "Gupta",
            "employee_email": "neha@sanskar.io",
            "phone": "+91 9876543214",
            "date_of_birth": "1995-07-14",
            "date_of_joining": "2022-04-01",
            "department": "Finance",
            "designation": "Finance Manager",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "B+",
            "skills": [
                {"skill": "Accounting", "proficiency": "Expert", "years_of_experience": 6},
                {"skill": "SQL", "proficiency": "Intermediate", "years_of_experience": 3},
            ]
        },
        {
            "first_name": "Vikram",
            "last_name": "Singh",
            "employee_email": "vikram@sanskar.io",
            "phone": "+91 9876543215",
            "date_of_birth": "1994-09-22",
            "date_of_joining": "2021-11-15",
            "department": "Operations",
            "designation": "Operations Manager",
            "employee_status": "Active",
            "annual_leave_balance": 24,
            "blood_group": "O+",
            "skills": [
                {"skill": "Leadership", "proficiency": "Advanced", "years_of_experience": 5},
                {"skill": "Communication", "proficiency": "Expert", "years_of_experience": 7},
            ]
        }
    ]

    for emp_data in employees_data:
        existing = frappe.db.get_value("Employee", {"employee_email": emp_data["employee_email"]}, "name")
        if not existing:
            skills = emp_data.pop("skills", [])
            doc = frappe.get_doc({
                "doctype": "Employee",
                **emp_data
            })
            for s in skills:
                doc.append("skills", s)
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Employee: {doc.full_name} ({doc.name})")
        else:
            print(f" [-] Employee already exists for email: {emp_data['employee_email']}")


def seed_leave_requests():
    """Seeds standard leave requests with appropriate user ownership."""
    config = frappe.get_single("Leave Configuration")
    orig_allow_backdated = config.allow_backdated_leave
    config.allow_backdated_leave = 1
    config.save(ignore_permissions=True)

    try:
        karan = frappe.db.get_value("Employee", {"employee_email": "karan@sanskar.io"}, "name")
        ravi = frappe.db.get_value("Employee", {"employee_email": "ravi@sanskar.io"}, "name")
        priya = frappe.db.get_value("Employee", {"employee_email": "priya@sanskar.io"}, "name")
        amit = frappe.db.get_value("Employee", {"employee_email": "amit@sanskar.io"}, "name")
        neha = frappe.db.get_value("Employee", {"employee_email": "neha@sanskar.io"}, "name")
        vikram = frappe.db.get_value("Employee", {"employee_email": "vikram@sanskar.io"}, "name")

        requests = []
        if ravi:
            requests.append({
                "employee": ravi,
                "owner_email": "ravi@sanskar.io",
                "from_date": "2026-04-20",
                "to_date": "2026-04-22",
                "leave_type": "Casual Leave",
                "reason": "Family function",
                "status": "Approved",
            })
        if amit:
            requests.append({
                "employee": amit,
                "owner_email": "amit@sanskar.io",
                "from_date": "2026-04-25",
                "to_date": "2026-04-25",
                "leave_type": "Sick Leave",
                "reason": "Doctor appointment",
                "status": "Approved",
            })
        if karan:
            requests.append({
                "employee": karan,
                "owner_email": "karan@sanskar.io",
                "from_date": "2026-05-01",
                "to_date": "2026-05-05",
                "leave_type": "Earned Leave",
                "reason": "Vacation",
                "status": "Approved",
            })
        if priya:
            requests.append({
                "employee": priya,
                "owner_email": "priya@sanskar.io",
                "from_date": add_days(today(), 14),
                "to_date": add_days(today(), 16),
                "leave_type": "Casual Leave",
                "reason": "Personal work",
                "status": "Pending",
            })
        if neha:
            requests.append({
                "employee": neha,
                "owner_email": "neha@sanskar.io",
                "from_date": "2026-04-10",
                "to_date": "2026-04-12",
                "leave_type": "Casual Leave",
                "reason": "Family gathering",
                "status": "Approved",
            })
            requests.append({
                "employee": neha,
                "owner_email": "neha@sanskar.io",
                "from_date": add_days(today(), 25),
                "to_date": add_days(today(), 26),
                "leave_type": "Sick Leave",
                "reason": "Routine health checkup",
                "status": "Pending",
            })
        if vikram:
            requests.append({
                "employee": vikram,
                "owner_email": "vikram@sanskar.io",
                "from_date": "2026-04-05",
                "to_date": "2026-04-07",
                "leave_type": "Casual Leave",
                "reason": "Personal work",
                "status": "Approved",
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
                    "owner": req["owner_email"],
                })
                doc.insert(ignore_permissions=True)
                doc.db_set("owner", req["owner_email"])

                if req["status"] == "Approved":
                    doc.submit()
                print(f" [✓] Created Leave Request: {doc.name} for {doc.employee_name} (Owner: {req['owner_email']}, Status: {req['status']})")
            else:
                # Ensure owner is correctly set to employee email
                frappe.db.set_value("Leave Request", existing, "owner", req["owner_email"])
                print(f" [-] Leave Request already exists: {existing} (owner synced to {req['owner_email']})")
    finally:
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
    """Creates HR Admin and all individual Employee test users for multi-user evaluation."""
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
        u = frappe.get_doc("User", "hr_admin@sanskar.io")
        existing_roles = {r.role for r in u.roles}
        for r in ["HR Admin", "Desk User"]:
            if r not in existing_roles:
                u.append("roles", {"role": r})
        u.save(ignore_permissions=True)
        update_password("hr_admin@sanskar.io", "admin123")
        print(" [-] User hr_admin@sanskar.io roles & password updated.")

    # 2. Individual Employee users
    employee_users = [
        {"email": "karan@sanskar.io", "first_name": "Karan", "last_name": "Mistry"},
        {"email": "ravi@sanskar.io", "first_name": "Ravi", "last_name": "Patel"},
        {"email": "priya@sanskar.io", "first_name": "Priya", "last_name": "Shah"},
        {"email": "amit@sanskar.io", "first_name": "Amit", "last_name": "Desai"},
        {"email": "neha@sanskar.io", "first_name": "Neha", "last_name": "Gupta"},
        {"email": "vikram@sanskar.io", "first_name": "Vikram", "last_name": "Singh"},
    ]

    for eu in employee_users:
        if not frappe.db.exists("User", eu["email"]):
            emp_user = frappe.get_doc({
                "doctype": "User",
                "email": eu["email"],
                "first_name": eu["first_name"],
                "last_name": eu["last_name"],
                "send_welcome_email": 0,
                "roles": [{"role": "Employee"}, {"role": "Desk User"}],
            })
            emp_user.insert(ignore_permissions=True)
            update_password(eu["email"], "employee123")
            print(f" [✓] Created User: {eu['email']} (Password: employee123, Role: Employee)")
        else:
            u = frappe.get_doc("User", eu["email"])
            existing_roles = {r.role for r in u.roles}
            for r in ["Employee", "Desk User"]:
                if r not in existing_roles:
                    u.append("roles", {"role": r})
            u.save(ignore_permissions=True)
            update_password(eu["email"], "employee123")
            print(f" [-] User {eu['email']} roles & password updated.")


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
            "filters_json": "[]",
            "color": "#3b82f6",
            "is_public": 1,
        },
        {
            "name": "Active Employees",
            "label": "Active Employees",
            "function": "Count",
            "document_type": "Employee",
            "filters_json": '[["Employee","employee_status","=","Active"]]',
            "color": "#10b981",
            "is_public": 1,
        },
        {
            "name": "Pending Leave Requests",
            "label": "Pending Leave Requests",
            "function": "Count",
            "document_type": "Leave Request",
            "filters_json": '[["Leave Request","approval_status","=","Pending"]]',
            "color": "#f59e0b",
            "is_public": 1,
        },
        {
            "name": "Employees On Leave",
            "label": "Employees On Leave",
            "function": "Count",
            "document_type": "Employee",
            "filters_json": '[["Employee","employee_status","=","On Leave"]]',
            "color": "#ec4899",
            "is_public": 1,
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
            doc = frappe.get_doc("Number Card", c["name"])
            doc.is_public = 1
            doc.color = c["color"]
            doc.save(ignore_permissions=True)
            print(f" [-] Updated Number Card: {c['name']}")

    # 2. Dashboard Charts
    chart_roles = [{"role": "Employee"}, {"role": "HR Admin"}, {"role": "System Manager"}]
    charts = [
        {
            "chart_name": "Department Wise Employee Strength",
            "chart_type": "Group By",
            "document_type": "Employee",
            "group_by_based_on": "department",
            "group_by_type": "Count",
            "type": "Bar",
            "is_standard": 1,
            "is_public": 1,
            "module": "Employee Hub",
            "color": "#3b82f6",
            "filters_json": "[]",
            "roles": chart_roles,
        },
        {
            "chart_name": "Leave Requests by Type",
            "chart_type": "Group By",
            "document_type": "Leave Request",
            "group_by_based_on": "leave_type",
            "group_by_type": "Count",
            "type": "Bar",
            "is_standard": 1,
            "is_public": 1,
            "module": "Employee Hub",
            "color": "#8b5cf6",
            "filters_json": "[]",
            "roles": chart_roles,
        },
        {
            "chart_name": "Employees by Designation",
            "chart_type": "Group By",
            "document_type": "Employee",
            "group_by_based_on": "designation",
            "group_by_type": "Count",
            "type": "Bar",
            "is_standard": 1,
            "is_public": 1,
            "module": "Employee Hub",
            "color": "#f97316",
            "filters_json": "[]",
            "roles": chart_roles,
        },
        {
            "chart_name": "Employees by Department",
            "chart_type": "Group By",
            "document_type": "Employee",
            "group_by_based_on": "department",
            "group_by_type": "Count",
            "type": "Donut",
            "is_standard": 1,
            "is_public": 1,
            "module": "Employee Hub",
            "color": "#3b82f6",
            "filters_json": "[]",
            "roles": chart_roles,
        },
        {
            "chart_name": "Leave Requests by Status",
            "chart_type": "Group By",
            "document_type": "Leave Request",
            "group_by_based_on": "approval_status",
            "group_by_type": "Count",
            "type": "Donut",
            "is_standard": 1,
            "is_public": 1,
            "module": "Employee Hub",
            "color": "#10b981",
            "filters_json": "[]",
            "roles": chart_roles,
        },
    ]

    for ch in charts:
        if not frappe.db.exists("Dashboard Chart", ch["chart_name"]):
            roles = ch.pop("roles", [])
            doc = frappe.get_doc({
                "doctype": "Dashboard Chart",
                "is_standard": 1,
                "module": "Employee Hub",
                **ch,
            })
            for r in roles:
                doc.append("roles", r)
            doc.insert(ignore_permissions=True)
            print(f" [✓] Created Dashboard Chart: {ch['chart_name']}")
        else:
            doc = frappe.get_doc("Dashboard Chart", ch["chart_name"])
            doc.type = ch["type"]
            doc.is_public = 1
            doc.custom_options = None
            doc.color = ch["color"]
            doc.set("roles", [])
            for r in ch.get("roles", []):
                doc.append("roles", r)
            doc.save(ignore_permissions=True)
            print(f" [✓] Updated Dashboard Chart: {ch['chart_name']}")

    # 3. Ensure Workspace is loaded in database
    ws_path = frappe.get_app_path(
        "employee_hub", "employee_hub", "workspace", "employee_hub", "employee_hub.json"
    )
    if os.path.exists(ws_path):
        with open(ws_path, "r", encoding="utf-8") as f:
            ws_data = json.load(f)

        if frappe.db.exists("Workspace", "Employee Hub"):
            ws_doc = frappe.get_doc("Workspace", "Employee Hub")
            ws_doc.content = ws_data.get("content", ws_doc.content)

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
                })

            ws_doc.save(ignore_permissions=True)

            # Clear any user-specific workspace overrides so the public one is served
            frappe.db.delete("Workspace", {"name": ["like", "%Employee Hub%"], "for_user": ["!=", ""]})
            print(" [✓] Updated Workspace: Employee Hub (charts, cards, shortcuts fully reloaded).")

    # 4. Standard Dashboard document (viewable at /app/dashboard-view/Employee Hub Dashboard)
    all_dash_charts = [
        {"chart": "Department Wise Employee Strength", "width": "Full"},
        {"chart": "Leave Requests by Type", "width": "Half"},
        {"chart": "Employees by Designation", "width": "Half"},
        {"chart": "Employees by Department", "width": "Half"},
        {"chart": "Leave Requests by Status", "width": "Half"},
    ]

    if not frappe.db.exists("Dashboard", "Employee Hub Dashboard"):
        dash = frappe.get_doc({
            "doctype": "Dashboard",
            "dashboard_name": "Employee Hub Dashboard",
            "module": "Employee Hub",
            "is_standard": 1,
            "charts": all_dash_charts,
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
        for c in all_dash_charts:
            dash.append("charts", c)
        dash.save(ignore_permissions=True)
        print(" [✓] Updated Dashboard: Employee Hub Dashboard")


def seed_all_sample_data():
    """Master seeding function executed via bench execute."""
    print("--- Seeding Employee Hub Sample Data ---")
    frappe.db.delete("Custom DocPerm", {"parent": "Employee"})
    frappe.db.delete("User Permission")
    frappe.db.delete("Dashboard Chart", {"name": ["in", ["Leave Requests", "Leaves Taken", "Department-wise Employee Strength"]]})
    frappe.db.delete("Dashboard Chart Link", {"chart": ["in", ["Leave Requests", "Leaves Taken", "Department-wise Employee Strength"]]})
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
