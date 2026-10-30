# Copyright (c) 2026, Sanskar Trainee and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_days, today
from frappe.model.workflow import apply_workflow


def test_multi_user_isolation():
    print("\n==========================================")
    print("TEST 1: MULTI-USER DATA ISOLATION & PERMISSIONS")
    print("==========================================")

    # 1. Test Karan (Employee)
    frappe.set_user("karan@sanskar.io")
    print(f"Current user: {frappe.session.user}")

    karan_emp = frappe.db.get_value("Employee", {"employee_email": "karan@sanskar.io"}, "name")
    ravi_emp = frappe.db.get_value("Employee", {"employee_email": "ravi@sanskar.io"}, "name")
    print(f"Karan Employee ID: {karan_emp}, Ravi Employee ID: {ravi_emp}")

    # Test list visibility
    karan_leaves = frappe.get_list("Leave Request", fields=["name", "employee", "owner"])
    print(f"Karan sees {len(karan_leaves)} leave request(s):")
    for lr in karan_leaves:
        print(f"  - {lr.name}: Employee={lr.employee}, Owner={lr.owner}")
        assert lr.owner == "karan@sanskar.io", f"SECURITY BREACH: Karan saw a record owned by {lr.owner}!"
    print(" [✓] PASS: Karan can only view his own Leave Requests in list view.")

    # Test direct document access to Ravi's leave request
    ravi_leave = frappe.db.get_value("Leave Request", {"owner": "ravi@sanskar.io"}, "name")
    if ravi_leave:
        doc = frappe.get_doc("Leave Request", ravi_leave)
        try:
            doc.check_permission("read")
            assert False, f"SECURITY BREACH: Karan was able to read Ravi's Leave Request ({ravi_leave})!"
        except frappe.PermissionError:
            print(f" [✓] PASS: Karan is blocked with PermissionError when attempting to read Ravi's request ({ravi_leave}).")

    # Test attempting to apply leave for another employee (Ravi)
    try:
        fraudulent_lr = frappe.get_doc({
            "doctype": "Leave Request",
            "employee": ravi_emp,
            "leave_type": "Casual Leave",
            "from_date": add_days(today(), 15),
            "to_date": add_days(today(), 16),
            "reason": "Impersonation test",
        })
        fraudulent_lr.insert()
        assert False, "SECURITY BREACH: Karan was able to apply leave for Ravi!"
    except (frappe.ValidationError, frappe.PermissionError) as e:
        print(f" [✓] PASS: Server-side validation blocked Karan from applying leave for Ravi: {e}")

    # Test applying leave for Karan himself
    my_lr = frappe.get_doc({
        "doctype": "Leave Request",
        "employee": karan_emp,
        "leave_type": "Casual Leave",
        "from_date": add_days(today(), 30),
        "to_date": add_days(today(), 31),
        "reason": "Personal time off test",
    })
    my_lr.insert()
    print(f" [✓] PASS: Karan successfully created his own Leave Request ({my_lr.name}).")

    # Switch back to Administrator for cleanup
    frappe.set_user("Administrator")
    my_lr.delete(ignore_permissions=True)
    frappe.db.commit()


def test_workflow_and_reject_flow():
    print("\n==========================================")
    print("TEST 2: WORKFLOW TRANSITIONS, REJECTION & RESUBMISSION")
    print("==========================================")

    karan_emp = frappe.db.get_value("Employee", {"employee_email": "karan@sanskar.io"}, "name")

    # 1. Create a test leave request as Karan
    frappe.set_user("karan@sanskar.io")
    test_lr = frappe.get_doc({
        "doctype": "Leave Request",
        "employee": karan_emp,
        "leave_type": "Sick Leave",
        "from_date": add_days(today(), 40),
        "to_date": add_days(today(), 42),
        "reason": "Flu test",
    })
    test_lr.insert()
    frappe.db.commit()
    print(f"Created test Leave Request: {test_lr.name}, Owner: {test_lr.owner}, Status: {test_lr.approval_status}, DocStatus: {test_lr.docstatus}")

    # 2. Test Rejection without reason (must fail validation)
    frappe.set_user("hr_admin@sanskar.io")
    try:
        apply_workflow(test_lr, "Reject")
        assert False, "VALIDATION BREACH: Rejection succeeded without rejection_reason!"
    except frappe.ValidationError as e:
        print(f" [✓] PASS: Rejection rejected when rejection_reason is empty: {e}")

    # 3. Test Rejection with reason
    test_lr.rejection_reason = "Department has critical release during this window."
    test_lr.db_set("rejection_reason", test_lr.rejection_reason)
    apply_workflow(test_lr, "Reject")
    test_lr.reload()
    print(f" [✓] PASS: Workflow Reject executed. New Status: {test_lr.approval_status}, DocStatus: {test_lr.docstatus}")
    assert test_lr.approval_status == "Rejected"
    assert test_lr.docstatus == 0

    # 4. Test Resubmission (Rejected -> Resubmit -> Pending)
    frappe.set_user("karan@sanskar.io")
    apply_workflow(test_lr, "Resubmit")
    test_lr.reload()
    print(f" [✓] PASS: Resubmit executed by employee. New Status: {test_lr.approval_status}, DocStatus: {test_lr.docstatus}")
    assert test_lr.approval_status == "Pending"
    assert test_lr.docstatus == 0

    # 5. Test Approval by HR Admin (Pending -> Approve -> Approved, docstatus 1)
    frappe.set_user("hr_admin@sanskar.io")
    apply_workflow(test_lr, "Approve")
    test_lr.reload()
    print(f" [✓] PASS: Approve executed by HR Admin. New Status: {test_lr.approval_status}, DocStatus: {test_lr.docstatus}")
    assert test_lr.approval_status == "Approved"
    assert test_lr.docstatus == 1

    # Cleanup
    frappe.set_user("Administrator")
    test_lr.cancel()
    test_lr.delete()
    frappe.db.commit()


def test_id_card_pdf_generation():
    print("\n==========================================")
    print("TEST 3: ID CARD PRINT FORMAT & PDF RENDERING")
    print("==========================================")
    frappe.set_user("Administrator")
    emp = frappe.get_last_doc("Employee")
    if not emp:
        print(" [!] No employee found to test PDF.")
        return

    print(f"Testing ID Card generation for employee: {emp.first_name} {emp.last_name} ({emp.name})")
    
    # 1. Test HTML rendering
    html_content = frappe.get_print("Employee", emp.name, print_format="Employee ID Card", as_pdf=False)
    assert "<table" in html_content, "HTML does not use table layout!"
    assert "#1e3a8a" in html_content, "Solid header color #1e3a8a missing!"
    print(f" [✓] PASS: HTML rendered successfully ({len(html_content)} characters).")

    # 2. Test PDF binary generation if wkhtmltopdf is installed
    import shutil
    if shutil.which("wkhtmltopdf"):
        try:
            pdf_bytes = frappe.get_print("Employee", emp.name, print_format="Employee ID Card", as_pdf=True)
            assert len(pdf_bytes) > 1000, f"Generated PDF is unusually small ({len(pdf_bytes)} bytes)!"
            assert pdf_bytes.startswith(b"%PDF"), "Generated output is not a valid PDF file!"
            print(f" [✓] PASS: PDF generated cleanly via wkhtmltopdf ({len(pdf_bytes)} bytes).")
        except Exception as e:
            print(f" [X] FAIL: PDF generation error: {e}")
            raise e
    else:
        print(" [i] NOTE: wkhtmltopdf binary is not installed in this Linux environment. HTML print layout validated (table-based, cross-platform compatible).")


def test_dashboard_charts_and_report():
    print("\n==========================================")
    print("TEST 4: DASHBOARD CHARTS & ANALYTICS REPORT")
    print("==========================================")
    frappe.set_user("Administrator")

    # 1. Check all dashboard charts exist and have valid configuration
    expected_charts = [
        ("Department Wise Employee Strength", "Bar"),
        ("Leave Requests by Type", "Bar"),
        ("Employees by Designation", "Bar"),
        ("Employees by Department", "Donut"),
        ("Leave Requests by Status", "Donut"),
    ]

    for chart_name, expected_type in expected_charts:
        assert frappe.db.exists("Dashboard Chart", chart_name), f"Dashboard Chart '{chart_name}' missing!"
        chart_doc = frappe.get_doc("Dashboard Chart", chart_name)
        assert chart_doc.type == expected_type, f"Chart '{chart_name}' type mismatch: expected {expected_type}, got {chart_doc.type}"
        print(f" [✓] PASS: Dashboard Chart '{chart_name}' verified (Visual Type: {chart_doc.type}, Aggregation: {chart_doc.chart_type})")

    # 2. Check Department-wise Employee Summary Report
    from employee_hub.employee_hub.report.department_wise_employee_summary.department_wise_employee_summary import execute
    columns, data, message, chart = execute()
    print(f" [✓] PASS: Department-wise Employee Summary Report executed successfully: {len(data)} department rows returned.")
    for row in data:
        print(f"     * {row['department']}: Total={row['total_employees']}, Active={row['active_employees']}, Avg Leave={row.get('avg_leave_balance', 0)}, Top Skill={row.get('top_skill', '-')}")


def run_full_verification():
    print("==========================================")
    print("STARTING FULL END-TO-END VERIFICATION")
    print("==========================================")
    test_multi_user_isolation()
    test_workflow_and_reject_flow()
    test_id_card_pdf_generation()
    test_dashboard_charts_and_report()
    print("\n==========================================")
    print("ALL 4 CRITICAL VERIFICATION TEST SUITES PASSED!")
    print("==========================================")


if __name__ == "__main__":
    run_full_verification()
