import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate


class ResearchProject(Document):

    def validate(self):
        self.validate_dates()
        self.validate_budget()
        self.set_project_code()

    def validate_dates(self):
        if self.end_date and self.start_date:
            if getdate(self.end_date) < getdate(self.start_date):
                frappe.throw(_("End Date cannot be before Start Date"))

    def validate_budget(self):
        if self.budget and self.budget < 0:
            frappe.throw(_("Budget cannot be negative"))

    def set_project_code(self):
        if not self.project_code:
            self.project_code = frappe.generate_hash(length=8).upper()

    def before_submit(self):
        if self.status not in ("Active", "Completed"):
            frappe.throw(_("Only Active or Completed projects can be submitted"))

    def on_submit(self):
        self.update_milestone_status()
        frappe.publish_realtime("project_submitted", {"project": self.name})

    def on_cancel(self):
        self.status = "Cancelled"

    def update_milestone_status(self):
        for ms in self.milestones:
            if ms.status == "Pending":
                ms.status = "In Progress"
        self.save()


def on_submit(doc, method=None):
    doc.update_milestone_status()


def on_cancel(doc, method=None):
    doc.status = "Cancelled"
    doc.save()
