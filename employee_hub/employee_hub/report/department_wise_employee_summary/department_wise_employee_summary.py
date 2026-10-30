# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    """
    Script Report entry point:
    Returns (columns, data, message, chart, report_summary) for Department Wise Employee Summary.
    """
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data, filters.get("chart_type") or "Bar")

    return columns, data, None, chart


def get_columns():
    """Defines columns displayed in the summary report table."""
    return [
        {
            "fieldname": "department",
            "label": _("Department"),
            "fieldtype": "Link",
            "options": "Department",
            "width": 180,
        },
        {
            "fieldname": "total_employees",
            "label": _("Total Employees"),
            "fieldtype": "Int",
            "width": 140,
        },
        {
            "fieldname": "active_employees",
            "label": _("Active Employees"),
            "fieldtype": "Int",
            "width": 140,
        },
        {
            "fieldname": "inactive_terminated",
            "label": _("Inactive / Terminated"),
            "fieldtype": "Int",
            "width": 170,
        },
        {
            "fieldname": "avg_leave_balance",
            "label": _("Avg Leave Balance"),
            "fieldtype": "Float",
            "precision": 1,
            "width": 150,
        },
        {
            "fieldname": "top_skill",
            "label": _("Top Skill (Most Common)"),
            "fieldtype": "Data",
            "width": 190,
        },
    ]


def get_data(filters):
    """
    Executes SQL queries with GROUP BY and JOINs to compute aggregate stats
    for all organizational departments and identify the most prevalent skill.
    Uses LEFT JOIN from tabDepartment to ensure all active departments are represented.
    """
    conditions = []
    params = {}

    if filters.get("department"):
        conditions.append("d.department_name = %(department)s")
        params["department"] = filters.get("department")

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    # Status condition for employee counting
    status_filter = filters.get("employee_status")
    emp_status_cond = ""
    if status_filter:
        emp_status_cond = "AND e.employee_status = %(status)s"
        params["status"] = status_filter

    # 1. Aggregate main statistics across all departments using LEFT JOIN
    summary_query = f"""
        SELECT
            d.department_name AS department,
            COUNT(CASE WHEN e.name IS NOT NULL {emp_status_cond} THEN e.name END) AS total_employees,
            SUM(CASE WHEN e.employee_status = 'Active' THEN 1 ELSE 0 END) AS active_employees,
            SUM(CASE WHEN e.employee_status IN ('Inactive', 'Terminated') THEN 1 ELSE 0 END) AS inactive_terminated,
            ROUND(COALESCE(AVG(CASE WHEN e.name IS NOT NULL {emp_status_cond} THEN e.annual_leave_balance END), 0), 1) AS avg_leave_balance
        FROM `tabDepartment` d
        LEFT JOIN `tabEmployee` e ON e.department = d.department_name
        {where_clause}
        GROUP BY d.department_name
        ORDER BY total_employees DESC, d.department_name ASC
    """

    dept_stats = frappe.db.sql(summary_query, params, as_dict=True)

    # 2. Compute the top skill per department using JOIN between tabEmployee and tabEmployee Skill
    skills_conditions = []
    if filters.get("department"):
        skills_conditions.append("e.department = %(department)s")
    if status_filter:
        skills_conditions.append("e.employee_status = %(status)s")

    where_skills = ("WHERE " + " AND ".join(skills_conditions)) if skills_conditions else ""

    top_skills_query = f"""
        SELECT
            e.department,
            es.skill,
            COUNT(es.name) AS skill_count
        FROM `tabEmployee` e
        INNER JOIN `tabEmployee Skill` es ON es.parent = e.name
        {where_skills}
        GROUP BY e.department, es.skill
        ORDER BY e.department ASC, skill_count DESC
    """

    skills_data = frappe.db.sql(top_skills_query, params, as_dict=True)

    # Map the top skill (highest count) for each department
    department_top_skill = {}
    for item in skills_data:
        dept = item.get("department")
        if dept and dept not in department_top_skill:
            department_top_skill[dept] = item.get("skill")

    # Combine metrics
    for row in dept_stats:
        dept_name = row.get("department")
        row["top_skill"] = department_top_skill.get(dept_name, _("None Registered"))

    return dept_stats


def get_chart_data(data, chart_type="Bar"):
    """
    Generates dynamic chart configuration supporting multiple representations:
    Bar, Donut, Pie, Line, and Percentage.
    """
    if not data:
        return None

    labels = [row.get("department") or _("Unassigned") for row in data]
    total_counts = [row.get("total_employees", 0) for row in data]
    active_counts = [row.get("active_employees", 0) for row in data]

    chart_type_lower = chart_type.lower()

    if chart_type_lower in ["pie", "donut", "percentage"]:
        return {
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "name": _("Employees"),
                        "values": total_counts,
                    }
                ],
            },
            "type": chart_type_lower,
            "colors": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"],
        }

    # For Bar and Line charts, show comparative series (Total vs Active)
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": _("Total Employees"),
                    "values": total_counts,
                },
                {
                    "name": _("Active Employees"),
                    "values": active_counts,
                },
            ],
        },
        "type": "line" if chart_type_lower == "line" else "bar",
        "colors": ["#3b82f6", "#10b981"],
    }
