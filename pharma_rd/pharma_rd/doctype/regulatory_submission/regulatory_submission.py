import frappe
from frappe import _
from frappe.model.document import Document


class RegulatorySubmission(Document):

    def before_save(self):
        if not self.submission_id:
            count = frappe.db.count("Regulatory Submission") + 1
            agency = (self.regulatory_agency or "REG")[:3].upper()
            stype  = (self.submission_type or "SUB")[:3].upper()
            self.submission_id = f"{agency}-{stype}-{count:04d}"

    def validate(self):
        from frappe.utils import getdate, today
        if self.actual_submission and self.status == "Draft":
            frappe.throw(_("Cannot set Actual Submission Date while status is Draft"))

    def on_submit(self):
        self.status = "Submitted"
        frappe.db.set_value(self.doctype, self.name, "status", "Submitted")
