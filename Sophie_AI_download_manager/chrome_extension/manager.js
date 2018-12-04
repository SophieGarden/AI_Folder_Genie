/*
FLASK API response:

A renderer for the response data will be selected using content negotiation based
on the client 'Accept' header. If you're making the API request from a regular client,
this will default to a JSON response.
*/


	chrome.downloads.onDeterminingFilename.addListener(function(downloadItem, suggest) {
		var file_name = downloadItem.filename;
		chrome.extension.getBackgroundPage().console.log(file_name);

			chrome.storage.sync.get(['key'], function(dirs) {
			var	dirs = dirs.key
			//chrome.extension.getBackgroundPage().console.log(dirs);

			var root_dir = dirs[0]
		  var downloads_dir = dirs[1]
			chrome.extension.getBackgroundPage().console.log(root_dir);
			chrome.extension.getBackgroundPage().console.log(downloads_dir);

		$.ajax({
		  url: "http://localhost:5000/",
		  type: "POST", //send it through post method
			//data: {file_name: file_name},
			data: {file_name: file_name,
						 root_dir: root_dir,
						 downloads_dir: downloads_dir
						},

		  success: function(result) {
				chrome.extension.getBackgroundPage().console.log(result);

		    suggest({filename: result});
		  },
		  error: function(xhr) {
				//chrome.extension.getBackgroundPage().console.log(errorThrown);
				chrome.extension.getBackgroundPage().console.log('wrong');
		    //suggest({filename: "mysubdirectory/" + file_name});
		  }
	  });


	});
	return true;

});
