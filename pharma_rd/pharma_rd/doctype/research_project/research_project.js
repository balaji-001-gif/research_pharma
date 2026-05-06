// Research Project — Client Script
frappe.ui.form.on("Research Project", {
    refresh: function(frm) {
        pharma_rd.colour_status_badge(frm);

        // Quick-action buttons
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Drug Candidates"), function() {
                frappe.set_route("List", "Drug Candidate", { research_project: frm.doc.name });
            }, __("Navigate"));

            frm.add_custom_button(__("View Clinical Trials"), function() {
                frappe.set_route("List", "Clinical Trial", { research_project: frm.doc.name });
            }, __("Navigate"));

            frm.add_custom_button(__("Add Compound"), function() {
                frappe.new_doc("Drug Candidate", { research_project: frm.doc.name });
            }, __("Create"));
        }

        // Progress bar for milestones
        frm.dashboard.reset();
        if (frm.doc.milestones && frm.doc.milestones.length) {
            const total     = frm.doc.milestones.length;
            const completed = frm.doc.milestones.filter(m => m.status === "Completed").length;
            frm.dashboard.add_progress(
                __("Milestone Progress"),
                Math.round((completed / total) * 100)
            );
        }

        // Budget utilisation
        if (frm.doc.budget && frm.doc.spent_budget) {
            const pct = Math.round((frm.doc.spent_budget / frm.doc.budget) * 100);
            const colour = pct > 90 ? "red" : pct > 70 ? "orange" : "green";
            frm.dashboard.add_comment(
                `Budget Utilisation: ${pct}%`, colour, true
            );
        }
    },

    end_date: function(frm) {
        if (frm.doc.end_date && frm.doc.start_date) {
            if (frm.doc.end_date < frm.doc.start_date) {
                frappe.throw(__("End Date cannot be before Start Date"));
                frm.set_value("end_date", "");
            }
        }
    },

    status: function(frm) {
        pharma_rd.colour_status_badge(frm);
    },
});
