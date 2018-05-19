$(".btn-fill-submit").click(insertOneTemplate);

function insertOneTemplate(event) {
	event.preventDefault();
	var submission = $(".form-fill-template").serializeArray();
	var results = ""
    $.each(submission, function(i, field) {
    	if (field.name() == "")
    });	
}