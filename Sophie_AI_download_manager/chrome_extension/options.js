
function saveOptions() {
  var pathInput1 = document.getElementById("root_dir_input");
  var root_dir = pathInput1.value;

  var pathInput2 = document.getElementById("downloads_dir_input");
  var downloads_dir = pathInput2.value;


  console.log('new root dir: '+root_dir);
  console.log('new downloads dir: '+downloads_dir);

  var dirs = [root_dir, downloads_dir];


  chrome.storage.sync.set({key: dirs}, function() {


    // Update status to let user know options were saved.
    var status = document.getElementById('status');
    status.textContent = 'Root and Downloads Directories Saved';
    // setTimeout(function() {
    //   status.textContent = '';
    // }, 1500);
    });

  chrome.storage.sync.get(['key'], function(result) {
    console.log('Get Directories' );
    console.log(result.key);
  });
}

function awesomeTask() {
  saveOptions();
}

function clickHandler(e) {
  setTimeout(awesomeTask, 800);
}

// Add event listeners once the DOM has fully loaded by listening for the
// `DOMContentLoaded` event on the document, and adding your listeners to
// specific elements when it triggers.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('button').addEventListener('click', clickHandler);
  //main();
});
