"""Scheduled tasks for Pharma R&D module."""
import frappe
from frappe import _
from frappe.utils import today, add_days, getdate


def check_expiry_alerts():
    """Daily: alert on batch expiries within 30 days."""
    alert_date = add_days(today(), 30)
    batches = frappe.get_all(
        "Batch Manufacturing Record",
        filters={
            "expiry_date": ["between", [today(), alert_date]],
            "batch_status": ["in", ["Released", "Passed"]],
        },
        fields=["name", "batch_no", "drug_candidate", "expiry_date", "batch_status"],
    )
    if not batches:
        return

    lab_managers = frappe.get_all(
        "Has Role",
        filters={"role": "Lab Manager", "parenttype": "User"},
        pluck="parent",
    )
    if not lab_managers:
        return

    rows = "".join(
        f"<tr><td>{b['batch_no']}</td><td>{b['drug_candidate']}</td><td>{b['expiry_date']}</td></tr>"
        for b in batches
    )
    frappe.sendmail(
        recipients=lab_managers,
        subject=f"Batch Expiry Alert — {len(batches)} batch(es) expiring within 30 days",
        message=f"<p>The following batches are expiring within 30 days:</p>"
                f"<table border='1' cellpadding='5'><tr><th>Batch</th><th>Drug</th><th>Expiry</th></tr>"
                f"{rows}</table>",
    )


def check_trial_milestones():
    """Daily: flag overdue clinical trial milestones."""
    overdue = frappe.db.sql("""
        SELECT ct.name, ct.trial_id, ct.trial_title, ct.status
        FROM `tabClinical Trial` ct
        WHERE ct.docstatus = 1
          AND ct.status = 'Active'
          AND ct.primary_completion < %s
    """, today(), as_dict=True)

    for trial in overdue:
        frappe.db.set_value("Clinical Trial", trial["name"], "status", "Data Collection")
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": "Clinical Trial",
            "reference_name": trial["name"],
            "content": f"Auto-updated: Primary completion date passed. Status changed to Data Collection.",
        }).insert(ignore_permissions=True)


def generate_stability_alerts():
    """Weekly: remind on upcoming stability timepoints."""
    alert_date = add_days(today(), 7)
    upcoming = frappe.db.sql("""
        SELECT ss.name AS study, ss.study_id, ss.drug_candidate, stp.timepoint, stp.target_date
        FROM `tabStability Study` ss
        INNER JOIN `tabStability Timepoint` stp ON stp.parent = ss.name
        WHERE ss.docstatus = 1
          AND ss.status = 'Ongoing'
          AND stp.status = 'Pending'
          AND stp.target_date BETWEEN %s AND %s
    """, (today(), alert_date), as_dict=True)

    if not upcoming:
        return

    qc_analysts = frappe.get_all(
        "Has Role",
        filters={"role": "QC Analyst", "parenttype": "User"},
        pluck="parent",
    )
    if not qc_analysts:
        return

    rows = "".join(
        f"<tr><td>{tp['study_id']}</td><td>{tp['drug_candidate']}</td>"
        f"<td>{tp['timepoint']}</td><td>{tp['target_date']}</td></tr>"
        for tp in upcoming
    )
    frappe.sendmail(
        recipients=qc_analysts,
        subject=f"Stability Timepoints Due This Week — {len(upcoming)} pending",
        message=f"<p>The following stability timepoints are due within 7 days:</p>"
                f"<table border='1' cellpadding='5'><tr><th>Study</th><th>Drug</th><th>Timepoint</th><th>Target Date</th></tr>"
                f"{rows}</table>",
    )
