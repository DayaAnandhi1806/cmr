// Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["CMR Summary"] = {
	"filters": [
		{
			fieldname:"date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		},
	]
};
