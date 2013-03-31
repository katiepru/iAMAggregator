function validateForm() {
	var name = document.forms["mainform"]["_name"].value;
	if(name==null || name=="") {
		alert("Name must be filled out");
		return false;
	}
	var email = document.forms["mainform"]["_email"].value;
	if(email==null || name=="") {
		alert("Either email or phone must be filled out");
		return false;
	}
	$.ajax(
		{
			type : 'POST',
			url : '/ajax',
			data : { name : name,
					 email : email,
				   }
		}
	  ).done(function( returnData ){
		$("#gobutton").addClass("btn-success");
	  });

}
