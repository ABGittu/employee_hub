// Copyright (c) 2026, Sanskar Trainee and contributors
// For license information, please see license.txt

frappe.query_reports["Department Wise Employee Summary"] = {
    filters: [
        {
            fieldname: "department",
            label: __("Department"),
            fieldtype: "Link",
            options: "Department"
        },
        {
            fieldname: "employee_status",
            label: __("Employee Status"),
            fieldtype: "Select",
            options: "\nActive\nInactive\nOn Leave\nTerminated"
        },
        {
            fieldname: "chart_type",
            label: __("Chart Type"),
            fieldtype: "Select",
            options: "Bar\nDonut\nPie\nLine\nPercentage",
            default: "Bar"
        }
    ],

    // Override chart options to ensure integer counts without currency formatting
    format_chart_options(options) {
        options.tooltipOptions = {
            formatTooltipY: d => Math.round(d) + " " + __("Employees")
        };
        options.axisOptions = {
            shortenYAxisNumbers: false
        };
        return options;
    }
};
