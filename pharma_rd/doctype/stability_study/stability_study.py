import frappe
from frappe import _
from frappe.model.document import Document


class StabilityStudy(Document):

    def before_save(self):
        if not self.study_id:
            count = frappe.db.count("Stability Study") + 1
            self.study_id = f"STB-{count:05d}"

    def validate(self):
        self.validate_dates()
        self.check_overdue_timepoints()

    def validate_dates(self):
        from frappe.utils import getdate
        if self.planned_end and self.start_date:
            if getdate(self.planned_end) <= getdate(self.start_date):
                frappe.throw(_("Planned End Date must be after Start Date"))

    def check_overdue_timepoints(self):
        from frappe.utils import today, getdate
        for tp in self.timepoints:
            if tp.target_date and getdate(tp.target_date) < getdate(today()) and tp.status == "Pending":
                tp.status = "Overdue"
