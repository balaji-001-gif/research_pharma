import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days


class LabEquipment(Document):

    def validate(self):
        self.check_calibration_overdue()

    def check_calibration_overdue(self):
        if self.calibration_due and getdate(self.calibration_due) < getdate(today()):
            if self.status == "Operational":
                frappe.msgprint(
                    _("Calibration is overdue for {0}. Status should be reviewed.").format(self.equipment_name),
                    indicator="orange",
                    title=_("Calibration Alert"),
                )
