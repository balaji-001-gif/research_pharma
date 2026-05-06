import frappe
from frappe.utils import add_days, nowdate, getdate
import random

def create_demo_data():
    print("Starting demo data creation...")
    
    # 1. Therapeutic Areas
    therapeutic_areas = [
        "Oncology", "Cardiology", "Neurology", "Immunology", 
        "Infectious Disease", "Metabolic Disorders", "Rare Diseases",
        "Respiratory", "Dermatology", "Ophthalmology"
    ]
    for area in therapeutic_areas:
        if not frappe.db.exists("Therapeutic Area", area):
            frappe.get_doc({
                "doctype": "Therapeutic Area",
                "area_name": area,
                "description": f"Research focused on {area} treatments."
            }).insert()
    print("Created Therapeutic Areas.")

    # 2. Biological Targets
    targets = [
        {"name": "HER2", "class": "Kinase", "uniprot": "P04626"},
        {"name": "EGFR", "class": "Kinase", "uniprot": "P00533"},
        {"name": "PD-L1", "class": "Other", "uniprot": "Q9NZQ7"},
        {"name": "ACE2", "class": "Other", "uniprot": "Q9BYF1"},
        {"name": "TNF-alpha", "class": "Other", "uniprot": "P01375"},
        {"name": "KRAS", "class": "Other", "uniprot": "P01116"}
    ]
    for t in targets:
        if not frappe.db.exists("Biological Target", t["name"]):
            frappe.get_doc({
                "doctype": "Biological Target",
                "target_id": t["name"],
                "target_name": t["name"],
                "target_class": t["class"],
                "uniprot_id": t["uniprot"]
            }).insert()
    print("Created Biological Targets.")

    # 3. Lab Equipment
    equipment = [
        {"id": "HPLC-01", "type": "Analytical", "name": "Agilent 1260 Infinity II"},
        {"id": "MS-02", "type": "Analytical", "name": "Thermo Orbitrap Exploris"},
        {"id": "NMR-01", "type": "Analytical", "name": "Bruker Avance III"},
        {"id": "INC-05", "type": "Biological", "name": "CO2 Incubator Heracell"},
        {"id": "FRZ-10", "type": "Storage", "name": "Ultra-Low Temp Freezer"}
    ]
    for e in equipment:
        if not frappe.db.exists("Lab Equipment", e["id"]):
            frappe.get_doc({
                "doctype": "Lab Equipment",
                "equipment_id": e["id"],
                "equipment_name": e["name"],
                "equipment_type": e["type"],
                "status": "Operational",
                "last_calibration": add_days(nowdate(), -30),
                "calibration_due": add_days(nowdate(), 335),
                "calibration_frequency": "Annual"
            }).insert()
    print("Created Lab Equipment.")

    # 4. Research Projects
    projects = [
        {"code": "PRJ-ONC-001", "title": "Next-Gen HER2 Inhibitors", "area": "Oncology", "phase": "Lead Optimization"},
        {"code": "PRJ-CRD-002", "title": "Novel ACE2 Modulators", "area": "Cardiology", "phase": "Hit-to-Lead"},
        {"code": "PRJ-NEU-003", "title": "Amyloid Beta Aggregation Blockers", "area": "Neurology", "phase": "Target Validation"},
        {"code": "PRJ-IMM-004", "title": "Selective JAK1 Inhibitors", "area": "Immunology", "phase": "Phase I"},
        {"code": "PRJ-INF-005", "title": "Pan-Coronavirus Vaccine Candidate", "area": "Infectious Disease", "phase": "Preclinical"}
    ]
    
    # Need a PI (Administrator by default for demo)
    pi = "Administrator"
    
    for p in projects:
        if not frappe.db.exists("Research Project", p["code"]):
            doc = frappe.get_doc({
                "doctype": "Research Project",
                "project_code": p["code"],
                "project_title": p["title"],
                "therapeutic_area": p["area"],
                "research_phase": p["phase"],
                "status": "Active",
                "priority": "High",
                "principal_investigator": pi,
                "start_date": add_days(nowdate(), -180),
                "budget": 5000000,
                "milestones": [
                    {"milestone_name": "Target Validation", "status": "Completed", "due_date": add_days(nowdate(), -150)},
                    {"milestone_name": "Lead Optimization", "status": "In Progress", "due_date": add_days(nowdate(), 30)}
                ]
            })
            doc.insert()
            if p["phase"] in ["Phase I", "Phase II", "Phase III"]:
                doc.submit()
    print("Created Research Projects.")

    # 5. Drug Candidates
    candidates = [
        {"id": "CPD-001", "name": "Trastuzumab Duo", "proj": "PRJ-ONC-001", "target": "HER2", "mw": 145000},
        {"id": "CPD-002", "name": "Neratinib Plus", "proj": "PRJ-ONC-001", "target": "EGFR", "mw": 557.1},
        {"id": "CPD-003", "name": "CardioMod-X", "proj": "PRJ-CRD-002", "target": "ACE2", "mw": 412.5},
        {"id": "CPD-004", "name": "Neuroprev-A", "proj": "PRJ-NEU-003", "target": "PD-L1", "mw": 380.2},
        {"id": "CPD-005", "name": "ImmunoSuppress-J", "proj": "PRJ-IMM-004", "target": "TNF-alpha", "mw": 425.6}
    ]
    for c in candidates:
        if not frappe.db.exists("Drug Candidate", c["id"]):
            frappe.get_doc({
                "doctype": "Drug Candidate",
                "compound_id": c["id"],
                "compound_name": c["name"],
                "research_project": c["proj"],
                "target": c["target"],
                "molecular_weight": c["mw"],
                "development_stage": "Lead",
                "patent_status": "Provisional Filed",
                "logp": 2.5,
                "psa": 75.0,
                "hbd": 2,
                "hba": 4
            }).insert()
    print("Created Drug Candidates.")

    # 6. Clinical Trials
    trials = [
        {"id": "TRIAL-I-001", "title": "Phase I Study of ImmunoSuppress-J", "cand": "CPD-005", "phase": "Phase I"},
        {"id": "TRIAL-II-002", "title": "Phase II Study of Trastuzumab Duo", "cand": "CPD-001", "phase": "Phase II"}
    ]
    for t in trials:
        if not frappe.db.exists("Clinical Trial", t["id"]):
            doc = frappe.get_doc({
                "doctype": "Clinical Trial",
                "trial_id": t["id"],
                "trial_title": t["title"],
                "drug_candidate": t["cand"],
                "trial_phase": t["phase"],
                "status": "Active",
                "irb_approval": 1,
                "irb_approval_date": add_days(nowdate(), -60),
                "planned_enrollment": 100,
                "start_date": add_days(nowdate(), -30),
                "sites": [
                    {"site_name": "General Hospital A", "pi_name": "Dr. Smith", "target_patients": 50, "site_status": "Enrolling"},
                    {"site_name": "Mayo Clinic", "pi_name": "Dr. Jones", "target_patients": 50, "site_status": "Initiated"}
                ]
            })
            doc.insert()
            doc.submit()
    print("Created Clinical Trials.")

    # 7. Batch Manufacturing Records (BMR)
    batches = [
        {"no": "BMR-2024-001", "cand": "CPD-001", "size": 10},
        {"no": "BMR-2024-002", "cand": "CPD-005", "size": 50}
    ]
    for b in batches:
        if not frappe.db.exists("Batch Manufacturing Record", b["no"]):
            doc = frappe.get_doc({
                "doctype": "Batch Manufacturing Record",
                "batch_no": b["no"],
                "drug_candidate": b["cand"],
                "batch_size": b["size"],
                "batch_unit": "kg",
                "manufacture_date": add_days(nowdate(), -15),
                "expiry_date": add_days(nowdate(), 730),
                "batch_status": "Pending QC",
                "batch_formula": [
                    {"ingredient": "Active Substance", "quantity": b["size"] * 0.1, "unit": "kg"},
                    {"ingredient": "Excipient A", "quantity": b["size"] * 0.9, "unit": "kg"}
                ],
                "process_steps": [
                    {"step_no": 1, "operation": "Mixing", "status": "Completed"},
                    {"step_no": 2, "operation": "Filtration", "status": "Completed"}
                ]
            })
            doc.insert()
            doc.submit()
    print("Created BMRs.")

    # 8. QC Tests
    tests = [
        {"id": "QCT-001", "batch": "BMR-2024-001", "type": "Assay", "result": "99.5%", "pass": "Pass"},
        {"id": "QCT-002", "batch": "BMR-2024-001", "type": "Purity", "result": "99.9%", "pass": "Pass"},
        {"id": "QCT-003", "batch": "BMR-2024-002", "type": "Sterility", "result": "Sterile", "pass": "Pass"}
    ]
    for t in tests:
        if not frappe.db.exists("QC Test", t["id"]):
            doc = frappe.get_doc({
                "doctype": "QC Test",
                "test_id": t["id"],
                "test_name": f"{t['type']} for {t['batch']}",
                "batch_no": t["batch"],
                "test_type": t["type"],
                "result_value": t["result"],
                "pass_fail": t["pass"],
                "analyst": "Administrator",
                "instrument": "HPLC-01",
                "test_date": nowdate()
            })
            doc.insert()
            doc.submit()
    print("Created QC Tests.")

    # 9. Stability Studies
    if not frappe.db.exists("Stability Study", "STB-001"):
        doc = frappe.get_doc({
            "doctype": "Stability Study",
            "study_id": "STB-001",
            "drug_candidate": "CPD-001",
            "batch_no": "BMR-2024-001",
            "study_type": "Long-Term",
            "temperature": "25°C",
            "humidity": "60%RH",
            "start_date": nowdate(),
            "timepoints": [
                {"timepoint": "Initial", "target_date": nowdate(), "status": "Completed"},
                {"timepoint": "3 Months", "target_date": add_days(nowdate(), 90), "status": "Pending"},
                {"timepoint": "6 Months", "target_date": add_days(nowdate(), 180), "status": "Pending"}
            ]
        })
        doc.insert()
        doc.submit()
    print("Created Stability Study.")

    # 10. Regulatory Submissions
    submissions = [
        {"id": "IND-2024-001", "type": "IND", "agency": "FDA", "cand": "CPD-005"},
        {"id": "CTA-2024-002", "type": "CTA", "agency": "EMA", "cand": "CPD-001"}
    ]
    for s in submissions:
        if not frappe.db.exists("Regulatory Submission", s["id"]):
            doc = frappe.get_doc({
                "doctype": "Regulatory Submission",
                "submission_id": s["id"],
                "submission_type": s["type"],
                "regulatory_agency": s["agency"],
                "drug_candidate": s["cand"],
                "status": "Submitted",
                "submission_date": add_days(nowdate(), -10)
            })
            doc.insert()
            doc.submit()
    print("Created Regulatory Submissions.")

    frappe.db.commit()
    print("Demo data creation completed successfully.")

if __name__ == "__main__":
    create_demo_data()
