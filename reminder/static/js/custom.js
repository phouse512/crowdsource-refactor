function submitWelcomePage(){
	name = $.trim($("#name").val());
	pin = $.trim($("#pin").val());
	phone = $.trim($("phone").val());

	results = validateInput(name, pin, phone);

	if(results == "valid input"){
		addUser(name, pin, phone);
	} else {
		console.log(results);
	}
}

function validateInput(name, pin, phone){
	if (!name.match(/^[0-9a-zA-z]+$/)){
  		return "invalid name";
  	} else if (!pin.match(/^[0-9]+$/)){
  		return "invalid pin";
  	} else if (!pin.match(/^[0-9]+$/)){
  		return "invalid phone";
  	} else {
  		return "valid input";
  	}
}

function addUser(name, pin, phone){
	$.ajax({
		type: 'POST',
		url: $SCRIPT_ROOT + '/welcome',
		data: ({ name: name,
				pin: pin,
				phone: phone}),
		success: function(data, textStatus, xhr){ 
			console.log('working!');
			console.log(data);
		},
		error: function(xhr, textStatus, errorThrown){
			console.log(errorThrown);
		}
	});
}