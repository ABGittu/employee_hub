app_name = "employee_hub"
app_title = "Employee Hub"
app_publisher = "Sanskar Trainee"
app_description = "Employee Hub System - Comprehensive HR & Leave Management Frappe App"
app_email = "trainee@sanskar.io"
app_license = "mit"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/employee_hub/css/employee_hub.css"
app_include_js = "/assets/employee_hub/js/employee_hub.js"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Employee": {
        "before_save": "employee_hub.employee_hub.doctype.employee.employee.set_full_name"
    }
}

# Fixtures
# --------
# Fixtures ensure system configuration (Custom Fields, Roles, Workflows)
# is tracked in git and automatically applied on fresh site install / bench migrate.

fixtures = [
    {
        "dt": "Role",
        "filters": [
            ["name", "in", ["HR Admin", "Employee"]]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "=", "Employee"],
            ["fieldname", "=", "blood_group"]
        ]
    },
    {
        "dt": "Workflow",
        "filters": [
            ["name", "=", "Leave Approval Workflow"]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            ["name", "in", ["Pending", "Approved", "Rejected", "Cancelled"]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["name", "in", ["Approve", "Reject", "Cancel", "Resubmit"]]
        ]
    }
]
