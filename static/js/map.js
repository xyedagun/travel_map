var baseUrl = 'http://localhost:5000';

function addPlaceToFolder(button, placeId) {
	var name = $('#' + placeId + '-name').text();
	var data = {name: name};

	$.post(baseUrl + '/add-to-folder', data, function(response) {
		button.text("Remove");
		var wasAdded = response['added'];
		alert("Done!")
		// if (wasAdded) {
		// 	// change to remove
		// } else {
		// 	// change to "Save to Folder"
		// }
		console.log("Got from the server: " + response);
	});
};



$(document).on('ready', function() {
	$('.yelpImage').on('click', function(evt){ //when you click on .yelpImage class, this function runs
		var thingTheyClickedOn = evt.currentTarget;//thingTheyClickedOn is the area where user can click within the yelpImage class
		var placeId = thingTheyClickedOn.id; // var placeId getting the ID of the place(rendered by jinja)
		var modalToShowId = 'modal' + placeId;//this variable is naming the modal adding the string "modal" and the id from YELP
		$('#'+ modalToShowId).modal(); //jquery: the id(#) plus the modalToShow, make a modal
		console.log('yo');

		var $saveButton = $('#' + placeId, '-save');
		$saveButton.on('click', function(e) {
			addPlaceToFolder($saveButton, placeId);
		});
	});

	$(".save-to-folder-button").on('click', addToFolder);
});

function addToFolder(evt){
	var thingTheyClickedOn = evt.currentTarget;
	var yelpId = $(thingTheyClickedOn).data('yelpId');
	//send a post resquest via AJAX!!!!! 
	//figure out which modal(use unique modal iD)/button they click on
	//make a js object, called postParams={"yelpId": modalId}:
	//send post request using AJAX
	//callback: change the button to text confirming action
	alert("Adding to Folder " + yelpId);
};




// $(document).on('ready', function(){
// 	$('.login-button').on('click', function(evt){
	

// 	});



// });


//need to to target specific div(container)




// add a class to each yelp each called "yelpimage"
// add an id for each image which is the yelp unique id
// using a jinja for-loop, make a modal for each yelp place. 
    // give each modal the id that is "modal" + yelpId