import frappe
from frappe import _
from frappe.model.document import Document


class DrugCandidate(Document):

    def validate(self):
        self.validate_lipinski()
        self.generate_compound_id()

    def generate_compound_id(self):
        if not self.compound_id:
            abbr = (self.research_project or "CMPD")[:4].upper()
            count = frappe.db.count("Drug Candidate") + 1
            self.compound_id = f"{abbr}-{count:04d}"

    def validate_lipinski(self):
        """Warn if Lipinski Rule-of-5 is violated."""
        violations = []
        if self.molecular_weight and self.molecular_weight > 500:
            violations.append("MW > 500")
        if self.logp and self.logp > 5:
            violations.append("LogP > 5")
        if self.hbd and self.hbd > 5:
            violations.append("HBD > 5")
        if self.hba and self.hba > 10:
            violations.append("HBA > 10")
        if violations:
            frappe.msgprint(
                _("Lipinski Rule-of-5 violations: {0}").format(", ".join(violations)),
                indicator="orange",
                title=_("Drug-likeness Warning"),
            )
