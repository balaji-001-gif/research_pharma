frappe.query_reports["Clinical Trial Status"] = {
    filters: [
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "\nDraft\nPlanning\nIRB/Ethics Pending\nActive\nEnrollment Complete\nData Collection\nAnalysis\nCompleted\nTerminated\nSuspended",
        },
        {
            fieldname: "trial_phase",
            label: __("Phase"),
            fieldtype: "Select",
            options: "\nPhase I\nPhase I/II\nPhase II\nPhase II/III\nPhase III\nPhase IV",
        },
    ],
};
