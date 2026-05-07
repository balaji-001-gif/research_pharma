app_name = "pharma_rd"
app_title = "Pharma RD"
app_publisher = "Your Company"
app_description = "Research and Pharma Development Application for Frappe v15+"
app_email = "admin@yourcompany.com"
app_license = "MIT"
app_version = "0.0.1"

# ------ App include files -------
# app_include_css = "/assets/pharma_rd/css/pharma_rd.css"
# app_include_js  = "/assets/pharma_rd/js/pharma_rd.js"

# ------ DocType class overrides -------
override_doctype_class = {}

# ------ Document Events -------
doc_events = {}

# ------ Scheduled Tasks -------
scheduler_events = {
    "daily": [
        "pharma_rd.tasks.check_expiry_alerts",
        "pharma_rd.tasks.check_trial_milestones",
    ],
    "weekly": [
        "pharma_rd.tasks.generate_stability_alerts",
    ],
}

# ------ Fixtures -------
fixtures = [
    {"dt": "Custom Field",   "filters": [["module", "=", "pharma_rd"]]},
    {"dt": "Property Setter","filters": [["module", "=", "pharma_rd"]]},
    {"dt": "Module Def",     "filters": [["name", "=", "pharma_rd"]]},
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
boot_session = "pharma_rd.boot.boot_session"
