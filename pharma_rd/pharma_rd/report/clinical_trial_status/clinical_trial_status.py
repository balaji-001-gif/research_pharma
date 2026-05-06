import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data    = get_data(filters)
    chart   = get_chart(data)
    summary = get_summary(data)
    return columns, data, None, chart, summary


def get_columns():
    return [
        {"fieldname": "trial_id",          "label": _("Trial ID"),           "fieldtype": "Link",     "options": "Clinical Trial", "width": 120},
        {"fieldname": "trial_title",       "label": _("Title"),              "fieldtype": "Data",     "width": 200},
        {"fieldname": "trial_phase",       "label": _("Phase"),              "fieldtype": "Data",     "width": 100},
        {"fieldname": "status",            "label": _("Status"),             "fieldtype": "Data",     "width": 130},
        {"fieldname": "drug_candidate",    "label": _("Drug Candidate"),     "fieldtype": "Link",     "options": "Drug Candidate", "width": 140},
        {"fieldname": "planned_enrollment","label": _("Planned N"),          "fieldtype": "Int",      "width": 100},
        {"fieldname": "actual_enrollment", "label": _("Enrolled N"),         "fieldtype": "Int",      "width": 100},
        {"fieldname": "enrollment_pct",    "label": _("Enrollment %"),       "fieldtype": "Percent",  "width": 110},
        {"fieldname": "start_date",        "label": _("Start Date"),         "fieldtype": "Date",     "width": 100},
        {"fieldname": "primary_completion","label": _("Primary Completion"), "fieldtype": "Date",     "width": 140},
        {"fieldname": "nct_number",        "label": _("NCT Number"),         "fieldtype": "Data",     "width": 130},
        {"fieldname": "irb_approval",      "label": _("IRB Approved"),       "fieldtype": "Check",    "width": 100},
        {"fieldname": "saes",              "label": _("SAEs"),               "fieldtype": "Int",      "width": 70},
    ]


def get_data(filters):
    conditions = ""
    if filters:
        if filters.get("status"):
            conditions += f" AND ct.status = '{filters['status']}'"
        if filters.get("trial_phase"):
            conditions += f" AND ct.trial_phase = '{filters['trial_phase']}'"

    data = frappe.db.sql(f"""
        SELECT
            ct.trial_id,
            ct.trial_title,
            ct.trial_phase,
            ct.status,
            ct.drug_candidate,
            ct.planned_enrollment,
            ct.actual_enrollment,
            ct.start_date,
            ct.primary_completion,
            ct.nct_number,
            ct.irb_approval,
            ct.saes
        FROM `tabClinical Trial` ct
        WHERE ct.docstatus < 2
        {conditions}
        ORDER BY ct.start_date DESC
    """, as_dict=True)

    for row in data:
        if row.planned_enrollment and row.actual_enrollment:
            row["enrollment_pct"] = round(
                (row.actual_enrollment / row.planned_enrollment) * 100, 1
            )
        else:
            row["enrollment_pct"] = 0.0
    return data


def get_chart(data):
    phase_counts = {}
    for row in data:
        phase_counts[row["trial_phase"]] = phase_counts.get(row["trial_phase"], 0) + 1
    return {
        "data": {
            "labels": list(phase_counts.keys()),
            "datasets": [{"name": "Trials by Phase", "values": list(phase_counts.values())}],
        },
        "type": "bar",
    }


def get_summary(data):
    total  = len(data)
    active = sum(1 for d in data if d["status"] == "Active")
    total_saes = sum((d["saes"] or 0) for d in data)
    return [
        {"value": total,      "label": _("Total Trials"),  "datatype": "Int"},
        {"value": active,     "label": _("Active Trials"), "datatype": "Int", "color": "green"},
        {"value": total_saes, "label": _("Total SAEs"),    "datatype": "Int", "color": "red"},
    ]
