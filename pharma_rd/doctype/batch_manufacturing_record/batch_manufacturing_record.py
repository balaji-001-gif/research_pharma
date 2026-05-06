import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, today


class BatchManufacturingRecord(Document):

    def before_save(self):
        if not self.batch_no:
            count = frappe.db.count("Batch Manufacturing Record") + 1
            self.batch_no = f"BMR-{count:06d}"

    def validate(self):
        self.validate_expiry()

    def validate_expiry(self):
        if self.expiry_date and self.manufacture_date:
            from frappe.utils import getdate
            if getdate(self.expiry_date) <= getdate(self.manufacture_date):
                frappe.throw(_("Expiry Date must be after Manufacture Date"))

    def on_submit(self):
        self.batch_status = "Pending QC"
        frappe.db.set_value(self.doctype, self.name, "batch_status", "Pending QC")


def on_submit(doc, method=None):
    doc.batch_status = "Pending QC"
    doc.save()
