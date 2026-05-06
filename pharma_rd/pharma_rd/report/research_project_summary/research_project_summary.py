import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    summary = get_summary(data)
    return columns, data, None, chart, summary


def get_columns():
    return [
        {"fieldname": "project_code",    "label": _("Project Code"),       "fieldtype": "Link",     "options": "Research Project", "width": 130},
        {"fieldname": "project_title",   "label": _("Title"),              "fieldtype": "Data",     "width": 220},
        {"fieldname": "therapeutic_area","label": _("Therapeutic Area"),   "fieldtype": "Link",     "options": "Therapeutic Area", "width": 150},
        {"fieldname": "research_phase",  "label": _("Phase"),              "fieldtype": "Data",     "width": 130},
        {"fieldname": "status",          "label": _("Status"),             "fieldtype": "Data",     "width": 100},
        {"fieldname": "priority",        "label": _("Priority"),           "fieldtype": "Data",     "width": 80},
        {"fieldname": "start_date",      "label": _("Start Date"),         "fieldtype": "Date",     "width": 100},
        {"fieldname": "end_date",        "label": _("End Date"),           "fieldtype": "Date",     "width": 100},
        {"fieldname": "budget",          "label": _("Budget"),             "fieldtype": "Currency", "width": 120},
        {"fieldname": "spent_budget",    "label": _("Spent"),              "fieldtype": "Currency", "width": 120},
        {"fieldname": "pi",              "label": _("Principal Investigator"), "fieldtype": "Link", "options": "User", "width": 140},
        {"fieldname": "milestone_count", "label": _("Milestones"),         "fieldtype": "Int",      "width": 90},
        {"fieldname": "completed_milestones","label": _("Completed"),      "fieldtype": "Int",      "width": 90},
    ]


def get_data(filters):
    conditions = build_conditions(filters)
    projects = frappe.db.sql(f"""
        SELECT
            rp.name             AS project_code,
            rp.project_title,
            rp.therapeutic_area,
            rp.research_phase,
            rp.status,
            rp.priority,
            rp.start_date,
            rp.end_date,
            rp.budget,
            rp.spent_budget,
            rp.principal_investigator AS pi
        FROM `tabResearch Project` rp
        WHERE rp.docstatus < 2
        {conditions}
        ORDER BY rp.start_date DESC
    """, as_dict=True)

    for p in projects:
        milestones = frappe.get_all(
            "Research Project Milestone",
            filters={"parent": p.project_code},
            fields=["status"],
        )
        p["milestone_count"] = len(milestones)
        p["completed_milestones"] = sum(1 for m in milestones if m.status == "Completed")

    return projects


def build_conditions(filters):
    if not filters:
        return ""
    cond = []
    if filters.get("status"):
        cond.append(f"rp.status = '{filters['status']}'")
    if filters.get("therapeutic_area"):
        cond.append(f"rp.therapeutic_area = '{filters['therapeutic_area']}'")
    if filters.get("from_date"):
        cond.append(f"rp.start_date >= '{filters['from_date']}'")
    if filters.get("to_date"):
        cond.append(f"rp.start_date <= '{filters['to_date']}'")
    return ("AND " + " AND ".join(cond)) if cond else ""


def get_chart(data):
    status_counts = {}
    for row in data:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{"name": "Projects by Status", "values": list(status_counts.values())}],
        },
        "type": "donut",
        "colors": ["#5e64ff", "#28a745", "#ffc107", "#dc3545", "#6c757d"],
    }


def get_summary(data):
    total = len(data)
    active = sum(1 for d in data if d["status"] == "Active")
    total_budget = sum((d["budget"] or 0) for d in data)
    total_spent  = sum((d["spent_budget"] or 0) for d in data)
    return [
        {"value": total,        "label": _("Total Projects"),    "datatype": "Int"},
        {"value": active,       "label": _("Active Projects"),   "datatype": "Int",      "color": "green"},
        {"value": total_budget, "label": _("Total Budget"),      "datatype": "Currency", "color": "blue"},
        {"value": total_spent,  "label": _("Total Spent"),       "datatype": "Currency", "color": "orange"},
    ]
