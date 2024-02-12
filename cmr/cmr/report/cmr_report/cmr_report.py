# Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
# For license information, please see license.txt

import frappe
import calendar
from datetime import datetime, timedelta

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": "RH/CH/Area Manager",
            "fieldtype": "Data",
            "fieldname": "created_user",
            "width": 140,
            "colspan": 2
        },
            {
                "label": "Meeting Target",
                "fieldtype": "Int",
                "fieldname": "meeting_target",
                "width": 120,
                
            },
            {
                "label": "Personal Meetings",
                "fieldtype": "Int",
                "fieldname": "personal_meetings",
                "width": 130,
                
            },
            {
                "label": "Client/Partner Event",
                "fieldtype": "Int",
                "fieldname": "client_or_partner_event",
                "width": 140,
                
            },
            {
                "label": "Total Meetings as per Weightage",
                "fieldtype": "Int",
                "fieldname": "total_meetings_as_per_weightage",
                "width": 150,
                
            },
            {
                "label": "Meeting Target",
                "fieldtype": "Int",
                "fieldname": "meeting_target1",
                "width": 120,
            },
            {
                "label": "Personal Meetings",
                "fieldtype": "Int",
                "fieldname": "personal_meetings1",
                "width": 140,
            },
            {
                "label": "Client/Partner Event",
                "fieldtype": "Int",
                "fieldname": "client_or_partner_event1",
                "width": 140,
            },
            {
                "label": "Total Meetings Done as per Weightage",
                "fieldtype": "Float",
                "fieldname": "total_meetings_done_as_per_weightage",
                "width": 150,
            },
            {
                "label": "New Clients",
                "fieldtype": "Int",
                "fieldname": "new_clients",
                "width": 120,
            },
            {
                "label": "Mapped Clients",
                "fieldtype": "Int",
                "fieldname": "mapped_clients",
                "width": 120,
            },
            {
                "label": "Meetings less than 4",
                "fieldtype": "Data",
                "fieldname": "meetings_less_than4",
                "width": 140,
            },
            {
                "label": "Meetings Greater than 4",
                "fieldtype": "Data",
                "fieldname": "meetings_greater_than4",
                "width": 140,
            }
    ]
    

    return columns

def get_data(filters):
    data = []
    per_meets = 0
    per_mon_meets = 0
    client_meets = 0
    tot_meets = 0
    client_mon_meets = 0
    tot_mon_meets = 0
    new_client_mon_meets = 0
    ex_client_mon_meets = 0
    less_meet = "No"
    greater_meet = "No"
    get_user = []
    input_date = datetime.strptime(filters.get("date"),'%Y-%m-%d')
    year = input_date.year
    month = input_date.month
    start_date = datetime(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = datetime(year, month, last_day)
    rm_list = frappe.db.get_all("CMR",filters={"date": filters.get("date")},pluck='owner')
    if rm_list:
        final_rm_list = list(set(rm_list))
        for usr in final_rm_list:
            cmr_doc_list = frappe.db.get_list("CMR", filters={"owner":usr,"date":filters.get("date")},pluck='name')
            for cmr in cmr_doc_list:
                cmr_doc = frappe.get_doc("CMR", cmr)
                if cmr_doc.meeting_with == "Customer":
                    per_meets += 1
                if cmr_doc.meeting_with == "Partner Alliance":
                    client_meets += 1
                tot_meets = per_meets + client_meets
                if tot_meets > 4:
                    greater_meet = "Yes"
                elif tot_meets < 4:
                    less_meet = "Yes"
            cmr_mon_doc_list = frappe.db.get_list("CMR",filters={"owner": usr,"date":["between",[start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')]]},pluck='name')
            for cmr1 in cmr_mon_doc_list:
                cmr_doc = frappe.get_doc("CMR", cmr1)
                if cmr_doc.meeting_with == "Customer":
                    per_mon_meets += 1
                if cmr_doc.meeting_with == "Partner Alliance":
                    client_mon_meets += 1
                if cmr_doc.existing_new == "New":
                    new_client_mon_meets += 1
                if cmr_doc.existing_new == "Existing":
                    ex_client_mon_meets += 1
                tot_mon_meets = ((per_meets + client_meets) / 80) * 100
            data.append({
                "meeting_target": 4,
                "created_user": usr,
                "personal_meetings": per_meets,
                "client_or_partner_event": client_meets,
                "total_meetings_as_per_weightage": tot_meets,
                "meeting_target1": 80,
                "personal_meetings1": per_mon_meets,
                "client_or_partner_event1": client_mon_meets,
                "total_meetings_done_as_per_weightage": tot_mon_meets,
                "new_clients": new_client_mon_meets,
                "mapped_clients": ex_client_mon_meets,
                "meetings_less_than4": less_meet,
                "meetings_greater_than4": greater_meet
            })
            per_meets = 0
            per_mon_meets = 0
            client_meets = 0
            client_mon_meets = 0
            tot_meets = 0
            tot_mon_meets = 0
            new_client_mon_meets = 0
            ex_client_mon_meets = 0
            less_meet = ""
            greater_meet = ""
    else:
        rm_list1 = frappe.db.get_all("CMR",filters={"date": ["between",[start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')]]},pluck='owner')
        final_rm_list = list(set(rm_list1))
        for usr in final_rm_list:
            cmr_mon_doc_list = frappe.db.get_list("CMR",filters={"owner": usr,"date":["between",[start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')]]},pluck='name')
            for cmr1 in cmr_mon_doc_list:
                cmr_doc = frappe.get_doc("CMR", cmr1)
                if cmr_doc.meeting_with == "Customer":
                    per_mon_meets += 1
                if cmr_doc.meeting_with == "Partner Alliance":
                    client_mon_meets += 1
                if cmr_doc.existing_new == "New":
                    new_client_mon_meets += 1
                if cmr_doc.existing_new == "Existing":
                    ex_client_mon_meets += 1
                tot_mon_meets = ((per_meets + client_meets) / 80) * 100
            data.append({
                "meeting_target": 4,
                "created_user": usr,
                "personal_meetings": per_meets,
                "client_or_partner_event": client_meets,
                "total_meetings_as_per_weightage": tot_meets,
                "meeting_target1": 80,
                "personal_meetings1": per_mon_meets,
                "client_or_partner_event1": client_mon_meets,
                "total_meetings_done_as_per_weightage": tot_mon_meets,
                "new_clients": new_client_mon_meets,
                "mapped_clients": ex_client_mon_meets,
                "meetings_less_than4": less_meet,
                "meetings_greater_than4": greater_meet
            })
            per_meets = 0
            per_mon_meets = 0
            client_meets = 0
            client_mon_meets = 0
            tot_meets = 0
            tot_mon_meets = 0
            new_client_mon_meets = 0
            ex_client_mon_meets = 0
            less_meet = ""
            greater_meet = ""
    return data
