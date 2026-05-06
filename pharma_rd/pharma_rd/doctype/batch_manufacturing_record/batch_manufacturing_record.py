import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class BatchManufacturingRecord(Document):
    def on_submit(self):
        self.log_signature("Submitted")

    def log_signature(self, action):
        self.append("signatures", {
            "user": frappe.session.user,
            "timestamp": now_datetime(),
            "action": action,
            "hash": frappe.generate_hash(length=32)
        })
        self.db_update_all()
