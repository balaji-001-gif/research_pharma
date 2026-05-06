// Drug Candidate — Client Script
frappe.ui.form.on("Drug Candidate", {
    refresh: function(frm) {
        pharma_rd.colour_status_badge(frm);

        if (!frm.is_new()) {
            frm.add_custom_button(__("Lipinski Check"), function() {
                pharma_rd.check_lipinski(frm);
            });

            frm.add_custom_button(__("Create Stability Study"), function() {
                frappe.new_doc("Stability Study", { drug_candidate: frm.doc.name });
            }, __("Create"));
        }
    },

    molecular_weight: function(frm) { pharma_rd.check_lipinski(frm); },
    logp:             function(frm) { pharma_rd.check_lipinski(frm); },
    hbd:              function(frm) { pharma_rd.check_lipinski(frm); },
    hba:              function(frm) { pharma_rd.check_lipinski(frm); },
});
