# Employee Hub System (`employee_hub`)

> **Frappe Framework — Trainee Practical Assignment (Month 1 Completion Evaluation)**  
> **App Name:** `employee_hub`  
> **Target Framework:** Frappe v16 / v15 (Python 3.12+, MariaDB 10.6+)  

---

## 1. Project Overview

**Employee Hub** is a modular Frappe custom application built to streamline organizational human resource administration. It manages:
- **Master Data**: Departments, Designations, and Skills.
- **Transactional Records**: Employee directory with multi-skill child table endorsements.
- **Policy Enforcement**: Company-wide Leave Configuration (Single DocType).
- **Submittable Workflow**: Leave Requests with balance validation, overlap checks, multi-state approval workflows with resubmission, own-record security, and automatic balance deduction/restoration.
- **Reporting & Visualization**: Script Report with SQL aggregation and charts, alongside a portable, wkhtmltopdf-compatible ID Card Print Format (Table layout + solid colors).

---

## 2. DocType List & Specifications

The following DocTypes (+ child table + single) are implemented:

| # | DocType | Type | Naming Strategy | Key Fields / Responsibilities |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Department** | Master | `field:department_name` | `department_name`, `department_head`, `is_active`, `description`. Validates no duplicate department names (case-insensitive). |
| **2** | **Designation** | Master | `field:designation_name` | `designation_name`, `department` (Link), `level` (Select: Junior/Mid/Senior/Lead/Manager), `is_active`, `description`. |
| **3** | **Skill** | Master | `field:skill_name` | `skill_name`, `skill_category` (Technical, Soft Skill, Domain, Tool), `is_active`, `description`. |
| **4** | **Employee** | Transactional | `naming_series:` (`EMP-.YYYY.-.#####`) | `first_name`, `last_name`, `full_name`, `employee_email`, `phone`, `date_of_birth`, `date_of_joining`, `department`, `designation`, `reporting_manager`, `employee_status`, `annual_leave_balance`, `profile_photo`, `address`, `skills` (Child Table). Enforces age $\ge$ 18, date validations, email syntax. |
| **5** | **Employee Skill** | Child Table (`istable: 1`) | Random hash | `skill` (Link), `proficiency` (Beginner/Intermediate/Advanced/Expert), `years_of_experience`, `notes`. |
| **6** | **Leave Configuration** | Single (`issingle: 1`) | Fixed (`Leave Configuration`) | `default_annual_balance`, `max_leave_days_per_request`, `allow_backdated_leave`, `max_casual_leave`, `max_sick_leave`, `max_earned_leave`. Configurable company policies. |
| **7** | **Leave Request** | Submittable (`is_submittable: 1`) | `naming_series:` (`LR-.YYYY.-.#####`) | `employee`, `employee_name`, `department`, `from_date`, `to_date`, `total_days`, `leave_type`, `reason`, `approval_status`, `approved_by`, `approval_date`, `rejection_reason`. Handles balance deduction and restoration on submit/cancel with own-record security. |

---

## 3. Assumptions

The application development is based on the following domain and technical principles:
1. **Annual Leave Cycle:** Assumes an annual allocation of 24 days (configurable via `Leave Configuration.default_annual_balance`).
2. **Leave Duration Calculation:** Uses standard inclusive day counting (`date_diff(to_date, from_date) + 1`).
3. **Approval Authority:** `HR Admin` acts as the primary approving and rejecting authority for employee leave requests.
4. **Employee Self-Service:** Employees can create draft leave requests for themselves, view only their own requests (`if_owner: 1`), and resubmit rejected requests back to pending.
5. **Backdated Applications:** Disallowed by default (`allow_backdated_leave = 0`), but configurable in `Leave Configuration`.
6. **Cross-Platform Print Compatibility:** ID Card print format uses pure HTML tables with solid HEX colors, eliminating wkhtmltopdf gradient, flexbox, and 50% border-radius rendering flaws.

---

## 4. Directory & File Structure Index

```
Employee Hub System/
├── pyproject.toml                                # App packaging metadata
├── setup.py                                      # Fallback setup configuration
├── requirements.txt                              # Python environment dependencies
├── README.md                                     # Project documentation & evaluation guide
├── license.txt                                   # Open-source MIT license
│
└── employee_hub/                                 # App Package Directory
    ├── __init__.py                               # Package init with __version__
    ├── hooks.py                                  # App hooks: doc_events, fixtures, includes
    ├── modules.txt                               # Declared modules ("Employee Hub")
    ├── patches.txt                               # Patch registry
    │
    ├── setup_sample_data.py                      # Seeding script for assessment data
    ├── test_verification.py                      # Automated test suite (isolation, workflow, PDF, charts)
    │
    ├── public/                                   # Client-side static assets
    │   ├── css/
    │   │   └── employee_hub.css                  # Status badge & indicator styling
    │   └── js/
    │       └── employee_hub.js                   # Desk boot script
    │
    ├── fixtures/                                 # JSON Fixtures (exported for bench migrate)
    │   ├── custom_field.json                     # blood_group field on Employee
    │   ├── role.json                             # HR Admin and Employee roles
    │   ├── workflow_state.json                   # Pending, Approved, Rejected, Cancelled
    │   ├── workflow_action_master.json           # Approve, Reject, Cancel, Resubmit
    │   └── workflow.json                         # Leave Approval Workflow definition
    │
    └── employee_hub/                             # "Employee Hub" Module
        ├── doctype/
        │   ├── department/                       # Master DocType
        │   │   ├── department.json
        │   │   ├── department.py                 # Case-insensitive duplicate validation
        │   │   └── department.js
        │   ├── designation/                      # Master DocType
        │   │   ├── designation.json
        │   │   ├── designation.py                # Active department link validation
        │   │   └── designation.js
        │   ├── skill/                            # Master DocType
        │   │   ├── skill.json
        │   │   ├── skill.py
        │   │   └── skill.js
        │   ├── employee_skill/                   # Child Table DocType
        │   │   ├── employee_skill.json
        │   │   └── employee_skill.py
        │   ├── employee/                         # Transactional DocType
        │   │   ├── employee.json                 # Core employee schema
        │   │   ├── employee.py                   # Age >= 18, doj not future, doj > dob
        │   │   ├── employee.js                   # Dynamic filter, custom buttons, dialog
        │   │   └── employee_list.js              # Custom status indicator pills
        │   ├── leave_configuration/              # Single DocType
        │   │   ├── leave_configuration.json      # Global leave limits & policies
        │   │   ├── leave_configuration.py
        │   │   └── leave_configuration.js
        │   └── leave_request/                    # Submittable DocType
        │       ├── leave_request.json            # Submittable schema, own-record rule
        │       ├── leave_request.py              # Balance checks, overlap prevention, submit/cancel, validation
        │       └── leave_request.js              # Balance intro, days calculation, before_workflow_action confirm/prompt
        │
        ├── dashboard_chart/
        │   ├── department_wise_employee_strength/ # Group By Department (Bar)
        │   ├── employees_by_department/           # Group By Department (Donut)
        │   ├── employees_by_designation/          # Group By Designation (Bar)
        │   ├── leave_requests_by_type/            # Group By Leave Type (Bar)
        │   └── leave_requests_by_status/          # Group By Approval Status (Donut)
        │
        ├── print_format/
        │   └── employee_id_card/                 # Table-based Jinja Print Format
        │       ├── employee_id_card.json
        │       └── employee_id_card.html         # Centered table badge layout (solid colors, wkhtmltopdf-safe)
        │
        └── report/
            └── department_wise_employee_summary/ # Script Report with SQL & Chart
                ├── department_wise_employee_summary.json
                ├── department_wise_employee_summary.py   # SQL GROUP BY + JOIN + Chart
                └── department_wise_employee_summary.js   # Department & Status filters
```

---

## 5. Workflow Lifecycle (Leave Approval Workflow)

The Leave Approval Workflow governs the lifecycle of `Leave Request`:

```
                       +-------------------+
                       |      Pending      | (docstatus = 0, Draft)
                       +-------------------+
                          |             |
           Approve (HR Admin)      Reject (HR Admin) [prompts reason]
                          |             |
                          v             v
       +--------------------+      +--------------------+
       |      Approved      |      |      Rejected      | (docstatus = 0, Draft)
       +--------------------+      +--------------------+
                 |                          |
          Cancel (HR Admin)          Resubmit (Employee / HR Admin)
                 |                          |
                 v                          v
       +--------------------+      +--------------------+
       |     Cancelled      |      |      Pending       |
       +--------------------+      +--------------------+
         (docstatus = 2)             (docstatus = 0)
```

### State & Action Matrix:

| Current State | Action | Allowed Role | Next State | Resulting `docstatus` | Permissions / Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pending** | `Approve` | HR Admin | **Approved** | `1` (Submitted) | Prompts `frappe.confirm()` summary in `before_workflow_action`. Deducts leave balance. |
| **Pending** | `Reject` | HR Admin | **Rejected** | `0` (Draft) | Prompts for mandatory `rejection_reason` via `frappe.prompt()`. Form becomes read-only. |
| **Approved** | `Cancel` | HR Admin | **Cancelled** | `2` (Cancelled) | Restores leave balance to employee. Workflow state set cleanly to `"Cancelled"`. |
| **Rejected** | `Resubmit` | Employee, HR Admin | **Pending** | `0` (Draft) | Clears rejection reason and re-opens request in `Pending` state for revision. |

### Key Workflow Protections:
- **Confirmation on Workflow Approval:** Placed in `before_workflow_action(frm)` instead of `before_submit`, ensuring it is triggered when approving via the workflow action button.
- **Mandatory Rejection Reason:** When HR Admin clicks `Reject`, a prompt modal enforces entering a `rejection_reason`. Server-side validation in `leave_request.py` also strictly forbids `Rejected` status without a reason.
- **Non-Editable Rejected State:** While in `Rejected` state, direct edits and saving are blocked on both client (`frm.disable_save()`) and server (`validate()`). To modify, the employee clicks `Resubmit`.
- **Clean Cancellation:** `on_cancel()` sets `approval_status = "Cancelled"`, eliminating conflicts where cancellation was formerly overwritten with `"Rejected"`.

---

## 6. Role Permissions & Own-Record Isolation

### Employee Role Permissions
1. **Own-Record Rule (`if_owner: 1`):** In `leave_request.json`, the `Employee` role has `"if_owner": 1`. Frappe automatically appends ``tabLeave Request`.`owner` = frappe.session.user` to queries. Employees never see other colleagues' leave requests.
2. **Fresh Site Independent:** Privacy does **not** rely on User Permissions created by seed scripts. It functions out-of-the-box on clean installations.
3. **No Direct Submit:** The `Employee` role has `"submit": 0`. Employees can only save drafts in `Pending` state; approvals and submissions are restricted to `HR Admin`.
4. **Server-Side Validation:** `validate_employee_own_record()` in `leave_request.py` prevents employees from applying on behalf of another employee ID.

---

## 7. ID Card PDF Print Format

The `Employee ID Card` print format is designed for universal rendering across both modern browsers and headless PDF engines (`wkhtmltopdf` / WeasyPrint):
- **Layout:** Rebuilt entirely using nested HTML tables with explicit widths (`width="330"`, `align="center"`).
- **Centering:** Enclosed in a 100% width wrapper table with `align="center"`, ensuring the card is centered on printed pages without relying on flexbox.
- **Solid Colors:** Uses solid HEX backgrounds (`#1e3a8a` for header, `#ffffff` for card body, `#f8fafc` for footer), avoiding wkhtmltopdf gradient dropouts.
- **Avatar Styling:** Centered inside a `<td>` with vertical and horizontal alignment (`align="center" valign="middle"`). Uses clean 8px corner radii (`border-radius: 8px`) to prevent wkhtmltopdf's known `50%` octagon rendering bug.
- **Initials Alignment:** Text is aligned via table cell vertical alignment and `line-height`, ensuring initials are centered.

---

## 8. Step-by-Step Bench Setup & Comprehensive Testing Guide

### 8.1 Setup on a Fresh Site
```bash
# 1. Switch to bench directory
cd /home/abhijit/frappe/hr-bench

# 2. Run migrations to apply doctypes and fixtures
bench --site hr.localhost migrate

# 3. Seed assessment sample data (departments, employees, test users, charts)
bench --site hr.localhost execute employee_hub.setup_sample_data.seed_all_sample_data
```

### 8.2 Test Accounts & Credentials

The seed script creates distinct test accounts with linked employee records for multi-user evaluation:

| Account | Roles | Linked Employee Record | Password |
| :--- | :--- | :--- | :--- |
| **`Administrator`** | System Manager, Administrator | Full System Access | `root` |
| **`hr_admin@sanskar.io`** | HR Admin, System Manager, Desk User | Supervisory / Approver | `admin123` |
| **`karan@sanskar.io`** | Employee, Desk User | Karan Patel (`EMP-2026-00001`) | `employee123` |
| **`ravi@sanskar.io`** | Employee, Desk User | Ravi Sharma (`EMP-2026-00002`) | `employee123` |
| **`priya@sanskar.io`** | Employee, Desk User | Priya Shah (`EMP-2026-00003`) | `employee123` |
| **`amit@sanskar.io`** | Employee, Desk User | Amit Desai (`EMP-2026-00004`) | `employee123` |

### 8.3 Automated Full Verification Suite

To verify all requirements (isolation, workflow, rejection prompt, resubmission, PDF layout, charts, reports) in one command:

```bash
bench --site hr.localhost execute employee_hub.test_verification.run_full_verification
```

### 8.4 Testing Checklist & How to Verify Each Requirement

#### 1. Testing Employee Role Isolation (Own-Record Rule)
- **Goal:** Verify that an employee user sees only their own leave requests and cannot submit on behalf of others.
- **Test in UI:**
  1. Log in as `karan@sanskar.io` (Password: `employee123`).
  2. Navigate to **Leave Request** list.
  3. Verify that only Karan's leave requests are displayed (Ravi, Priya, and Amit's requests are hidden).
  4. Click **New**: verify `Employee` field defaults to Karan and cannot be altered.
  5. Verify there is **no** Submit button; only Save (Draft) is available.
- **Automated CLI Verification:**
  ```bash
  bench --site hr.localhost execute employee_hub.test_verification.test_multi_user_isolation
  ```

#### 2. Testing Confirm Dialog on Workflow Approval
- **Goal:** Verify `frappe.confirm` triggers when approving via workflow.
- **Test in UI:**
  1. Log in as `hr_admin@sanskar.io` (Password: `admin123`) or `Administrator`.
  2. Open any `Pending` Leave Request.
  3. Click **Actions -> Approve**.
  4. Verify the confirmation popup appears displaying the employee name, dates, total days, and leave balance deduction warning.
  5. Click **Cancel**: verify submission is aborted and document remains `Pending`.
  6. Click **Actions -> Approve** and click **Yes**: verify document status becomes `Approved` (`docstatus = 1`) and days are deducted.

#### 3. Testing Reject Flow & Reason Prompt
- **Goal:** Verify mandatory rejection reason, read-only rejected state, and resubmission.
- **Test in UI:**
  1. Open a `Pending` Leave Request as `HR Admin`.
  2. Click **Actions -> Reject**.
  3. Verify a prompt dialog opens asking for **Rejection Reason**.
  4. Close dialog: verify rejection is aborted.
  5. Re-open and enter reason (e.g. `"Overlap with team release"`), submit.
  6. Verify document status is `Rejected` with `docstatus = 0`.
  7. Verify the form fields cannot be edited and the standard **Save** button is disabled.
  8. Click **Actions -> Resubmit**: verify document returns to `Pending` and fields become editable again.

#### 4. Testing Cancellation State Integrity
- **Goal:** Verify cancelling an approved request does not overwrite the status with `"Rejected"`.
- **Test in UI:**
  1. Open an `Approved` Leave Request.
  2. Click **Actions -> Cancel**.
  3. Verify `approval_status` is `"Cancelled"` (`docstatus = 2`).
  4. Verify the employee's `annual_leave_balance` is credited back.

#### 5. Testing ID Card PDF Layout
- **Goal:** Verify print format renders with visible header, centered card, and aligned avatar.
- **Test in UI:**
  1. Navigate to **Employee** list and open any employee (e.g., Karan Mistry).
  2. Click **Print** (printer icon) and select **Employee ID Card**.
  3. Verify:
     - Header has solid dark blue background (`#1e3a8a`) with crisp white title.
     - Card is centered horizontally.
     - Avatar box is square with rounded corners (no octagon distortion).
     - Employee initials / photo are aligned.
     - Blood group badge and employee details table align cleanly.
  4. Click **PDF**: verify the rendered PDF looks identical to preview.

#### 6. Testing Dashboard Charts & Summary Report
- **Goal:** Verify that bar charts and report analytics compute and display properly.
- **Test in UI:**
  1. Open `/app/employee-hub` Workspace:
     - Verify Number Cards: Total Employees, Active Employees, Pending Leave Requests, Employees On Leave.
     - Verify Bar Charts: **Leave Requests by Type** (`#8b5cf6`), **Employees by Designation** (`#f97316`), and **Department Wise Employee Strength** (`#2563eb`).
     - Verify Donut Charts: **Employees by Department** and **Leave Requests by Status**.
  2. Open `/app/dashboard-view/Employee Hub Dashboard`:
     - Verify all 5 charts render seamlessly.
  3. Open `/app/query-report/Department Wise Employee Summary`:
     - Verify department breakdown table displays columns: Department, Total Employees, Active Employees, Inactive/Terminated, Avg Leave Balance, and Top Skill.
     - Toggle department filter and chart type (Bar vs Donut) to ensure dynamic responsiveness.

---

## 9. Evaluation Q&A Preparation

### Q1: Why did you use `before_workflow_action` instead of `before_submit` for the confirmation prompt?
- In Frappe, when a workflow is active, approving a document calls `frappe.model.workflow.apply_workflow` via an API request directly on the server.
- The standard form `frm.save("Submit")` and its client event `before_submit` are completely bypassed by workflow action clicks.
- By binding `frappe.confirm()` to `before_workflow_action(frm)` and returning a `Promise`, we intercept the workflow action button click, unfreeze the DOM, present the confirmation modal, and only resolve the promise (allowing `apply_workflow` to proceed) when the user confirms.

### Q2: Why does "Rejected" use `docstatus = 0` (Draft) rather than `docstatus = 2` (Cancelled)?
- In Frappe's architecture, a document can only transition to `docstatus = 2` (Cancelled) from `docstatus = 1` (Submitted). Attempting a direct transition from `docstatus = 0` (Draft) to `docstatus = 2` triggers an `Illegal Document Status` exception.
- Marking `Rejected` as `docstatus = 0` preserves the draft status while keeping the document locked via workflow state permissions (`allow_edit: "System Manager"` and client-side `frm.disable_save()`).
- This enables a clean `Resubmit` workflow action allowing employees to re-open their request without having to re-type a new document from scratch.

### Q3: Why is `if_owner: 1` better than relying solely on User Permissions created by the seed script?
- User Permissions require manual or script-driven creation for every user on every site. If a fresh site is set up or a new employee account is added, missing User Permissions would leak all organization-wide leave requests to that employee.
- Configuring `"if_owner": 1` in `leave_request.json` embeds ownership isolation directly into Frappe's role permission engine, guaranteeing own-record security out-of-the-box on every bench site.

### Q4: Why rebuild the ID Card using HTML tables instead of CSS Flexbox and gradients?
- Frappe PDF generation relies on `wkhtmltopdf` (Qt WebKit) which lacks reliable support for modern CSS3 flexbox and linear gradients, resulting in invisible headers, collapsed containers, off-center positioning, and polygonal octagon distortions on `border-radius: 50%`.
- Rebuilding the card with nested HTML tables (`align="center"`, `valign="middle"`), solid HEX colors, and explicit pixel dimensions ensures 100% pixel-perfect rendering across browser desk preview, wkhtmltopdf, WeasyPrint, and remote backup restores.
