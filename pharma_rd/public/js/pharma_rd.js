/* Pharma R&D — Global Client Script */
frappe.provide("pharma_rd");

pharma_rd = {
    // Utility: colour status badges
    colour_status_badge: function(frm) {
        const statusMap = {
            "Active": "green", "Passed": "green", "Approved": "green", "Released": "green",
            "Failed": "red",   "Rejected": "red",  "Terminated": "red", "Overdue": "red",
            "On Hold": "orange","Suspended": "orange","Pending": "grey","Draft": "grey",
            "Completed": "blue","Submitted": "blue",
        };
        const status = frm.doc.status || frm.doc.batch_status || frm.doc.pass_fail || "";
        const colour = statusMap[status] || "grey";
        frm.page.set_indicator(status, colour);
    },

    // Utility: format currency compactly
    format_compact_currency: function(value) {
        if (Math.abs(value) >= 1e6)  return (value / 1e6).toFixed(1) + "M";
        if (Math.abs(value) >= 1e3)  return (value / 1e3).toFixed(1) + "K";
        return value.toFixed(2);
    },

    // Check Lipinski Rule-of-5 client-side
    check_lipinski: function(frm) {
        const violations = [];
        if (frm.doc.molecular_weight > 500) violations.push("MW > 500 Da");
        if (frm.doc.logp            >   5) violations.push("LogP > 5");
        if (frm.doc.hbd             >   5) violations.push("H-Bond Donors > 5");
        if (frm.doc.hba             >  10) violations.push("H-Bond Acceptors > 10");
        if (violations.length) {
            frm.dashboard.add_comment(
                "⚠ Lipinski Rule-of-5 violations: " + violations.join(", "),
                "yellow", true
            );
        } else {
            frm.dashboard.add_comment("✓ Passes Lipinski Rule-of-5", "green", true);
        }
    },
};

// Apply colour badges globally on form refresh
$(document).on("frappe.form.refresh", function() {
    if (cur_frm) pharma_rd.colour_status_badge(cur_frm);
});
