import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class QCTest(Document):

    def before_save(self):
        if not self.test_id:
            count = frappe.db.count("QC Test") + 1
            self.test_id = f"QCT-{count:06d}"

    def validate(self):
        if self.pass_fail == "Pass":
            self.status = "Passed"
        elif self.pass_fail == "Fail":
            self.status = "Failed"
            self.create_oos_record()

    def create_oos_record(self):
        if not self.oos_reference:
            frappe.msgprint(
                _("Test result is FAIL. Please create an OOS (Out of Specification) investigation record."),
                indicator="red",
                title=_("OOS Alert"),
            )

    def on_submit(self):
        self.log_signature("Submitted")
        if self.batch_no:
            self.update_batch_qc_status()

    def log_signature(self, action):
        self.append("signatures", {
            "user": frappe.session.user,
            "timestamp": now_datetime(),
            "action": action,
            "hash": frappe.generate_hash(length=32)
        })
        self.db_update_all()

    def update_batch_qc_status(self):
        batch = frappe.get_doc("Batch Manufacturing Record", self.batch_no)
        all_tests = frappe.get_all(
            "QC Test",
            filters={"batch_no": self.batch_no, "docstatus": 1},
            fields=["pass_fail"],
        )
        if any(t.pass_fail == "Fail" for t in all_tests):
            batch.qc_status = "Failed"
        elif all(t.pass_fail == "Pass" for t in all_tests):
            batch.qc_status = "Passed"
        else:
            batch.qc_status = "In Progress"
        batch.save()
