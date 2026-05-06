app_name = "pharma_rd"
app_title = "Pharma R&D"
app_publisher = "Your Company"
app_description = "Research and Pharmaceutical Development Management for ERPNext v15+"
app_email = "admin@yourcompany.com"
app_license = "MIT"
app_version = "0.0.1"

# ------ App include files -------
app_include_css = "/assets/pharma_rd/css/pharma_rd.css"
app_include_js  = "/assets/pharma_rd/js/pharma_rd.js"

# ------ DocType class overrides -------
override_doctype_class = {}

# ------ Document Events -------
doc_events = {
    "Research Project": {
        "on_submit":  "pharma_rd.pharma_rd.doctype.research_project.research_project.on_submit",
        "on_cancel":  "pharma_rd.pharma_rd.doctype.research_project.research_project.on_cancel",
    },
    "Clinical Trial": {
        "on_submit":  "pharma_rd.pharma_rd.doctype.clinical_trial.clinical_trial.on_submit",
    },
    "Batch Manufacturing Record": {
        "on_submit":  "pharma_rd.pharma_rd.doctype.batch_manufacturing_record.batch_manufacturing_record.on_submit",
    },
}

# ------ Scheduled Tasks -------
scheduler_events = {
    "daily": [
        "pharma_rd.pharma_rd.tasks.check_expiry_alerts",
        "pharma_rd.pharma_rd.tasks.check_trial_milestones",
    ],
    "weekly": [
        "pharma_rd.pharma_rd.tasks.generate_stability_alerts",
    ],
}

# ------ Fixtures -------
fixtures = [
    {"dt": "Custom Field",   "filters": [["module", "=", "Pharma R&D"]]},
    {"dt": "Property Setter","filters": [["module", "=", "Pharma R&D"]]},
    {"dt": "Role",           "filters": [["name", "in", [
        "Pharma Researcher", "Clinical Trial Manager",
        "QC Analyst", "Regulatory Affairs Officer",
        "Lab Manager", "Pharma Admin"
    ]]]},
]

# ------ Permissions -------
has_permission = {}

# ------ Portal menu items -------
portal_menu_items = []

# ------ Website Route Rules -------
website_route_rules = []

# ------ Boot Session -------
boot_session = "pharma_rd.pharma_rd.boot.boot_session"
