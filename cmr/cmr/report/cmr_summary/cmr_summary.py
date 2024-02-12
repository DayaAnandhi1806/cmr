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
            "label": "Date",
            "fieldtype": "Date",
            "fieldname": "date",
            "width": 140,
            "colspan": 2
        },
        {
            "label": "Meeting Start Time",
            "fieldtype": "Time",
            "fieldname": "meeting_start_time",
            "width": 120
            
        },
        {
            "label": "Meeting End Time",
            "fieldtype": "Time",
            "fieldname": "meeting_end_time",
            "width": 120
            
        },
        {
            "label": "Meeting Type",
            "fieldtype": "Data",
            "fieldname": "meeting_type",
            "width": 130,
            
        },
        {
            "label": "Emp.Code",
            "fieldtype": "Data",
            "fieldname": "emp_code",
            "width": 140,
            
        },
        {
            "label": "Emp Name",
            "fieldtype": "Data",
            "fieldname": "emp_name",
            "width": 150,
            
        },
        {
            "label": "Type",
            "fieldtype": "Data",
            "fieldname": "existing_new",
            "width": 120,
        },
        {
            "label": "Client/partner Code",
            "fieldtype": "Data",
            "fieldname": "code",
            "width": 140,
        },
        {
            "label": "Name",
            "fieldtype": "Data",
            "fieldname": "name",
            "width": 140,
        },
        {
            "label": "Mobile",
            "fieldtype": "Int",
            "fieldname": "mobile",
            "width": 150,
        },
        {
            "label": "Email Id",
            "fieldtype": "Data",
            "options":"Email",
            "fieldname": "email",
            "width": 120,
        },
        {
            "label": "Discussed about",
            "fieldtype": "Data",
            "fieldname": "summary",
            "width": 150,
        }
        
]

    

    return columns

def get_data(filters):
    data =[]
    all_data = frappe.db.get_all("CMR", filters={"date":filters.get("date")},fields=['date','meeting_start_time','meeting_end_time','meeting_type','code','existing_new','name','mobile','email','meeting_agenda','owner'])
    for details in all_data:
        emp_name, emp_code = get_employee_info(details['owner'])
        user= frappe.session.user
        frappe.errprint(details['owner'])
        # if user != "Administrator":     
        #frappe.errprint("hj")     
        if details['owner']=="Administrator":
            data.append({
                "emp_name" : "Admininstrator",
                "emp_code" : "",
                
                "date":details["date"],
                "meeting_start_time":details["meeting_start_time"],
                "meeting_end_time":details["meeting_end_time"],
                "meeting_type":details["meeting_type"],
                "existing_new":details["existing_new"],
                "name":details["name"],
                "mobile":details["mobile"], 
                "email":details["email"],
                #"summary":details["summary"],
                "code":details["code"],
                "summary":details["meeting_agenda"]
                
            })
        else:
            try:
                  
                cmr1= frappe.get_last_doc("Employee",filters={"user_id":details['owner']})
                if cmr1:            
                    frappe.errprint(cmr1.name)
                    data.append({
                        "emp_name" : cmr1.first_name,
                        "emp_code" : cmr1.name,
                        
                        "date":details["date"],
                        "meeting_start_time":details["meeting_start_time"],
                        "meeting_end_time":details["meeting_end_time"],
                        "meeting_type":details["meeting_type"],
                        "existing_new":details["existing_new"],
                        "name":details["name"],
                        "mobile":details["mobile"], 
                        "email":details["email"],
                        #"summary":details["summary"],
                        "code":details["code"],
                        "summary":details["meeting_agenda"]
                        
                    })
            except:
                data.append({
                "emp_name" : details['owner'],
                "emp_code" : "",
                
                "date":details["date"],
                "meeting_start_time":details["meeting_start_time"],
                "meeting_end_time":details["meeting_end_time"],
                "meeting_type":details["meeting_type"],
                "existing_new":details["existing_new"],
                "name":details["name"],
                "mobile":details["mobile"], 
                "email":details["email"],
                #"summary":details["summary"],
                "code":details["code"],
                "summary":details["meeting_agenda"]
                
            })
            
    return data

def get_employee_info(owner):
    # Implement logic to fetch employee information based on the owner (user ID)
    # You can use frappe.get_all or other methods to retrieve employee data
    # Replace the following dummy values with actual data retrieval logic
    emp_name = "Employee Name"
    emp_code = "Employee Code"
    return emp_name, emp_code