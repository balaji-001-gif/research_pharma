import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "test_id",     "label": _("Test ID"),      "fieldtype": "Link",  "options": "QC Test", "width": 120},
        {"fieldname": "test_name",   "label": _("Test Name"),    "fieldtype": "Data",  "width": 160},
        {"fieldname": "test_type",   "label": _("Type"),         "fieldtype": "Data",  "width": 140},
        {"fieldname": "batch_no",    "label": _("Batch"),        "fieldtype": "Link",  "options": "Batch Manufacturing Record", "width": 120},
        {"fieldname": "analyst",     "label": _("Analyst"),      "fieldtype": "Link",  "options": "User",    "width": 130},
        {"fieldname": "test_date",   "label": _("Test Date"),    "fieldtype": "Date",  "width": 100},
        {"fieldname": "result_value","label": _("Result"),       "fieldtype": "Data",  "width": 100},
        {"fieldname": "specification","label": _("Specification"),"fieldtype": "Data", "width": 130},
        {"fieldname": "pass_fail",   "label": _("Pass/Fail"),    "fieldtype": "Data",  "width": 90},
        {"fieldname": "status",      "label": _("Status"),       "fieldtype": "Data",  "width": 100},
    ]
    conditions = ""
    if filters:
        if filters.get("batch_no"):
            conditions += f" AND batch_no = '{filters['batch_no']}'"
        if filters.get("pass_fail"):
            conditions += f" AND pass_fail = '{filters['pass_fail']}'"
        if filters.get("from_date"):
            conditions += f" AND DATE(test_date) >= '{filters['from_date']}'"
        if filters.get("to_date"):
            conditions += f" AND DATE(test_date) <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT test_id, test_name, test_type, batch_no, analyst, test_date,
               result_value, specification, pass_fail, status
        FROM `tabQC Test`
        WHERE docstatus < 2
        {conditions}
        ORDER BY test_date DESC
    """, as_dict=True)
    return columns, data
