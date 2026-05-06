frappe.query_reports["Research Project Summary"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nDraft\nActive\nOn Hold\nCompleted\nCancelled",
        },
        {
            fieldname: "therapeutic_area",
            label: __("Therapeutic Area"),
            fieldtype: "Link",
            options: "Therapeutic Area",
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
        },
    ],
};
