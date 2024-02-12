# Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

        
def create_lead(doc, method):
    if doc.existing_new == 'New' and doc.meeting_with == 'Customer':
        existing_lead = frappe.db.exists('Lead', {'mobile_no': doc.mobile})
        if existing_lead:
            lead_name = frappe.db.get_value('Lead', {'mobile_no': doc.mobile}, 'lead_name')
            lead_link = frappe.utils.get_url_to_form('Lead', existing_lead)
            msg = f"Lead already exists: {lead_name}. <a href='{lead_link}'>View Lead</a>."
            frappe.msgprint(msg, alert=True, indicator='red', title='Information')

        else:
            lead = frappe.get_doc({
                'doctype': 'Lead',
                'lead_name': doc.name1,
                'mobile_no': doc.mobile,
                'email_id': doc.email
            })
            lead.insert(ignore_permissions=True)
            frappe.db.commit()
            lead_link = frappe.utils.get_url_to_form('Lead', lead.name)
            msg = f"Lead {lead.name} created successfully. <a href='{lead_link}'>View Lead</a>."
            frappe.msgprint(msg, alert=True, indicator='green', title='Success')

