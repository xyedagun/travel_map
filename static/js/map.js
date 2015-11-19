
$(document).on('ready', function() {
	$('.yelpImage').on('click', function(evt){ //when you click on .yelpImage class, this function runs
		var thingTheyClickedOn = evt.currentTarget;
		console.log(thingTheyClickedOn)		//thingTheyClickedOn is the area where user can click within the yelpImage class
		var placeId = thingTheyClickedOn.id;
		console.log(placeId) // var placeId getting the ID of the place(rendered by jinja)
		var modalToShowId = 'modal' + placeId;//this variable is naming the modal adding the string "modal" and the id from YELP
		$('#'+ modalToShowId).modal(); //jquery: the id(#) plus the modalToShow, make a modal
		console.log('yo');

		$('#' + modalToShowId).find(".save-to-folder-button").on('click', function(e) {
			addPlaceToFolder(e.currentTarget, placeId);
		});
	});
});


function addPlaceToFolder(folderElement, placeId) {
	var foldername = $(folderElement).text();
	var data = {"business_id": placeId,
				"folder_name": foldername};

	// debugger;

	$.post('/add-to-folder', data, function(response) {



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









// $(document).on('ready', function(){
// 	$('.login-button').on('click', function(evt){
	

// 	});



// });


//need to to target specific div(container)




// add a class to each yelp each called "yelpimage"
// add an id for each image which is the yelp unique id
// using a jinja for-loop, make a modal for each yelp place. 
    // give each modal the id that is "modal" + yelpId