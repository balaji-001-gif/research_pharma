// Clinical Trial — Client Script
frappe.ui.form.on("Clinical Trial", {
    refresh: function(frm) {
        pharma_rd.colour_status_badge(frm);

        if (!frm.is_new() && frm.doc.planned_enrollment) {
            const enrolled = frm.doc.actual_enrollment || 0;
            const pct = Math.round((enrolled / frm.doc.planned_enrollment) * 100);
            frm.dashboard.add_progress(
                __("Enrollment Progress") + ` (${enrolled} / ${frm.doc.planned_enrollment})`,
                pct
            );
        }

        if (!frm.is_new()) {
            frm.add_custom_button(__("View Regulatory Submissions"), function() {
                frappe.set_route("List", "Regulatory Submission", { drug_candidate: frm.doc.drug_candidate });
            }, __("Navigate"));
        }
    },

    planned_enrollment: function(frm) {
        if (frm.doc.planned_enrollment && frm.doc.planned_enrollment < 0) {
            frappe.throw(__("Planned Enrollment cannot be negative"));
        }
    },

    status: function(frm) {
        if (frm.doc.status === "Active" && !frm.doc.irb_approval) {
            frappe.msgprint({
                title: __("IRB Required"),
                message: __("IRB/Ethics Approval must be confirmed before setting status to Active."),
                indicator: "red",
            });
        }
    },
});
