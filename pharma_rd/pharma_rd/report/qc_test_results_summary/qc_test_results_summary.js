frappe.query_reports["QC Test Results Summary"] = {
    filters: [
        {fieldname:"batch_no",  label:__("Batch"),     fieldtype:"Link", options:"Batch Manufacturing Record"},
        {fieldname:"pass_fail", label:__("Pass/Fail"), fieldtype:"Select", options:"\nPass\nFail"},
        {fieldname:"from_date", label:__("From Date"), fieldtype:"Date"},
        {fieldname:"to_date",   label:__("To Date"),   fieldtype:"Date"},
    ],
};
