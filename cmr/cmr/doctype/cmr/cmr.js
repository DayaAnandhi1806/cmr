// Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('CMR', {
	meeting_start_time: function(frm) {
        let currentTime = moment().format('HH:mm:ss');
		var fieldElement = $('[data-fieldname="meeting_start_time"]');
        if (frm.doc.meeting_start_time > currentTime) {
			fieldElement.css('color', 'red');
            /* frappe.throw('Meeting start time cannot be later than the current time'); */
			frappe.validated = false;
            /* frm.set_value('meeting_start_time', '');
			frm.refresh_fields("meeting_end_time"); */
        }
		else
		{
			fieldElement.css('color', 'black');
		}
    },

	meeting_end_time: function(frm) {
        let currentTime = moment().format('HH:mm:ss');
		var fieldElement = $('[data-fieldname="meeting_end_time"]');
        if (frm.doc.meeting_end_time <= frm.doc.meeting_start_time || frm.doc.meeting_end_time > currentTime) {
			
			fieldElement.css('color', 'red');
            //frappe.throw('Meeting end time cannot be later than the current time/ earlier than start time');
			validated = false;
            /* frm.set_value('meeting_end_time', '');
			frm.refresh_fields("meeting_end_time"); */
        }
		else
		{
			fieldElement.css('color', 'black');
		}
    },
	onload: function(frm, cdt, cdn) {
		frm.set_query("meeting_with", function() {
			return {
				"filters": [["name", "in", ['Customer','Partner Alliance']]]
			};
		});
		frm.set_query("meeting_agenda", function() {
			return {
				"filters": [
					["CMR Meeting Agenda","meeting_with", "=", frm.doc.meeting_with],
					["CMR Meeting Agenda","existing_new", "=", frm.doc.existing_new]
				]
			};
		});
	},

	existing_new: function(frm) {
        if (frm.doc.existing_new === 'New') {
            frm.set_value('name1', '');  
            frm.set_value('mobile', '');
			frm.set_value('email','')
			frm.set_value('salutation','');
        }
		
		var meetingWithValue = frm.doc.meeting_with_new;
		var existingValue = frm.doc.existing_new;
		var options = [];

		if (meetingWithValue == "Customer" && existingValue == "Existing") {
			options = ["Product Discussion", "Followup Meeting", "Account Activation", "Documentation"];
		} else if (meetingWithValue == "Partner Alliance" && existingValue == "Existing") {
			options = ["Product Discussion","Follow up Meeting","Business Strategy/Lead Generation Discussion"];
		} else if (meetingWithValue == "Customer" && existingValue == "New") {
			options = ["Product Discussion", "Follow up Meeting", "Documention"];
		} else if (meetingWithValue == "Partner Alliance" && existingValue == "New") {
			options = ["Product Discussion","Follow up Meeting","Business Strategy/Commercials Discussion"];
		}

		frm.set_df_property('meeting_agenda', 'options', options);
    
    },
	code: function(frm){
		if(frm.doc.meeting_with === "Customer"){
			get_customer(frm)
		}
		if(frm.doc.meeting_with === "Branch"){
			get_partner(frm)
		}	
	},
	meeting_with_new: function(frm) {
		let meetingWith = frm.doc.meeting_with_new;
		frm.set_value('meeting_with', '')
		frm.set_value('code', ''); 
		frm.set_value('name1', '');  
        frm.set_value('mobile', '');
		frm.set_value('email','')
		frm.set_value('contact_person','')
		
		// console.log(frm.fields_dict['code'].df.fieldtype)

		var meetingWithValue = frm.doc.meeting_with_new;
		var existingValue = frm.doc.existing_new;
		var options = [];

		if (meetingWithValue ==  "Customer"){
			//console.log("cccchiiii000")
		frm.set_value('meeting_with', "Customer")
		frm.fields_dict['code'].get_query = function(doc, cdt, cdn) {
			return
		};
		frm.refresh_field('code');
		}
		if (meetingWithValue ==  "Partner Alliance"){
			// console.log("pppphiiii000")
		frm.set_value('meeting_with', "Branch")
		frm.fields_dict['code'].get_query = function(doc, cdt, cdn) {
			return {
				filters: [
					['Branch', 'fsl_branch_type', '=', 'AP']
				]
			};
		};
		frm.refresh_field('code');
		}


		if (meetingWithValue == "Customer" && existingValue == "Existing") {
			options = ["Product Discussion", "Followup Meeting", "Account Activation", "Documentation"];
		} else if (meetingWithValue == "Partner Alliance" && existingValue == "Existing") {
			options = ["Product Discussion","Follow up Meeting","Business Strategy/Lead Generation Discussion"];
		} else if (meetingWithValue == "Customer" && existingValue == "New") {
			options = ["Product Discussion", "Follow up Meeting", "Documention"];
		} else if (meetingWithValue == "Partner Alliance" && existingValue == "New") {
			options = ["Product Discussion","Follow up Meeting","Business Strategy/Commercials Discussion"];
			
		}

		frm.set_df_property('meeting_agenda', 'options', options);

	},

	// setBranchFilter: function(frm) {
	// 	frm.fields_dict['code'].get_query = function(doc, cdt, cdn) {
	// 		return {
	// 			filters: [
	// 				['Branch', 'fsl_branch_type', '=', 'AP']
	// 			]
	// 		};
	// 	};
	// 	frm.refresh_field('code');
	// },

	date: function(frm) {
		var selectedDate = frm.doc.date;
        var today = get_today();
        var dayBeforeYesterday = frappe.datetime.add_days(today, -1);
		if (selectedDate > today || selectedDate < dayBeforeYesterday) {
			frappe.throw('You can only select yesterday or current date in Date');
			frm.set_value('date', '');
			validated = false;
		}
    },

    before_save: function (frm) {

        let currentTime = moment().format('HH:mm:ss');
		var selectedDate = frm.doc.date;
        var today = get_today();
        var dayBeforeYesterday = frappe.datetime.add_days(today, -1);
		let followupDate = moment(frm.doc.followup_date_time).format('YYYY-MM-DD');
        let currentDate = moment(frm.doc.date).format('YYYY-MM-DD');
		
		if (selectedDate > today || selectedDate < dayBeforeYesterday) {
			frappe.throw('You can only select yesterday or current date in Date');
			frm.set_value('date', '');
			validated = false;
		}
        if (frm.doc.meeting_start_time >= currentTime) {
            frappe.throw('Meeting start time cannot be later than the current time');
            validated = false;
            frm.set_value('meeting_start_time', '');
        }
        if (frm.doc.meeting_end_time <= frm.doc.meeting_start_time || frm.doc.meeting_end_time > currentTime) {
            frappe.throw('Meeting end time cannot be later than the current time/ start time');
            validated = false;
            frm.set_value('meeting_end_time', '');
        }
		if(frm.doc.add_followup == true) 
		{
			if(moment(followupDate).isSameOrBefore(currentDate)) 
			{
            frappe.throw('Follow-up date and time must not be earlier than the Meeting date.');
            validated = false;
            frm.set_value('followup_date_time', '');
        	}
	}
    },

	followup_date_time: function(frm) {
		let followupDate = moment(frm.doc.followup_date_time).format('YYYY-MM-DD');
        let currentDate = moment(frm.doc.date).format('YYYY-MM-DD');
		let fieldElement = $('[data-fieldname="followup_date_time"]');

        if (moment(followupDate).isSameOrBefore(currentDate)) {
			fieldElement.css('color', 'red');
            //frappe.throw('Follow-up date and time must not be earlier than the Meeting date.');
            // validated = false;
            //frm.set_value('followup_date_time', '');
        }
		else
		{
			fieldElement.css('color', 'black');
		}
	},

	refresh: function(frm) {
		// console.log("hii")


        // frm.fields_dict['accompanied_with'].get_query = function(doc, cdt, cdn) {
		// 	console.log("hii87")
        //     // Fetch all Employee names dynamically
        //     return {
        //         query: 'cmr.cmr.doctype.cmr.cmr.get_all_employees'
        //     };
        // };
		frappe.call({
            method: 'cmr.cmr.doctype.cmr.cmr.get_all_employees',
            callback: function(r) {
                if (r.message) {
                    var employee_options = r.message;
                    frm.set_df_property('accompanied_with', 'options', employee_options);
                }
            }
        });
    }
	
});
async function get_customer(frm) {
	// console.log("hiiii00ccc0")
	const customer_data = await frappe.db.get_value('Customer', frm.doc.code, ['customer_name', 'mobile_no','email_id']);
	var data = customer_data.message;
	frm.set_value("name1",data.customer_name)
	frm.set_value("mobile",data.mobile_no)
	frm.set_value("email",data.email_id)
}
async function get_partner(frm) {
	// console.log("hiiii000")
	const customer_data = await frappe.db.get_value('Branch', frm.doc.code, ['branch', 'fsl_mobile_no','fsl_email','fsl_contact_person']);
	var data = customer_data.message;
	frm.set_value("name1",data.branch)
	frm.set_value("mobile",data.fsl_mobile_no)
	frm.set_value("email",data.fsl_email)
	frm.set_value("contact_person",data.fsl_contact_person)
}


