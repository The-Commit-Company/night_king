// Copyright (c) 2024, The Commit Company and contributors
// For license information, please see license.txt

frappe.ui.form.on("Night King", {
    refresh(frm) {

    },

    create_users(frm) {
        frm.call('create_raven_users')
    },
    generate_reactions(frm) {
        frm.call('generate_reactions')
    }
});
