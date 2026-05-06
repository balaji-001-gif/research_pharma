import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate


class ClinicalTrial(Document):

    def before_save(self):
        self.generate_trial_id()

    def generate_trial_id(self):
        if not self.trial_id:
            phase_abbr = self.trial_phase.replace(" ", "").replace("/", "") if self.trial_phase else "CT"
            count = frappe.db.count("Clinical Trial") + 1
            self.trial_id = f"{phase_abbr}-{count:04d}"

    def validate(self):
        self.validate_irb()
        self.validate_dates()

    def validate_irb(self):
        if self.status in ("Active", "Enrollment Complete", "Data Collection") and not self.irb_approval:
            frappe.throw(_("IRB/Ethics Approval is required before activating the trial"))

    def validate_dates(self):
        if self.primary_completion and self.start_date:
            if getdate(self.primary_completion) < getdate(self.start_date):
                frappe.throw(_("Primary Completion Date cannot be before Start Date"))

    def on_submit(self):
        frappe.publish_realtime("trial_submitted", {"trial": self.name})
        self.notify_regulatory()

    def notify_regulatory(self):
        regulatory_officers = frappe.get_all(
            "Has Role",
            filters={"role": "Regulatory Affairs Officer", "parenttype": "User"},
            pluck="parent",
        )
        for officer in regulatory_officers:
            try:
                frappe.sendmail(
                    recipients=[officer],
                    subject=f"Clinical Trial Submitted: {self.trial_id}",
                    message=f"Clinical Trial <b>{self.trial_title}</b> has been submitted for review.",
                )
            except frappe.OutgoingEmailError:
                frappe.msgprint(_("Regulatory notification skipped: Outgoing Email Account not configured."))
