// QC Test — Client Script
frappe.ui.form.on("QC Test", {
    refresh: function(frm) {
        const colour = frm.doc.pass_fail === "Pass" ? "green" : frm.doc.pass_fail === "Fail" ? "red" : "grey";
        frm.page.set_indicator(frm.doc.pass_fail || "Pending", colour);

        if (frm.doc.pass_fail === "Fail" && !frm.is_new()) {
            frm.dashboard.add_comment(
                __("⚠ OOS Investigation Required — This test has FAILED"), "red", true
            );
        }
    },

    pass_fail: function(frm) {
        const colour = frm.doc.pass_fail === "Pass" ? "green" : "red";
        frm.page.set_indicator(frm.doc.pass_fail, colour);
        if (frm.doc.pass_fail === "Fail") {
            frappe.msgprint({
                title: __("OOS Alert"),
                message: __("Test result is FAIL. Initiate an Out-of-Specification (OOS) investigation."),
                indicator: "red",
            });
        }
    },
});
