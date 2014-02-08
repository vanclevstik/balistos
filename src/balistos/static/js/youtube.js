// Your use of the YouTube API must comply with the Terms of Service:
// https://developers.google.com/youtube/terms

// Helper function to display JavaScript value on HTML page.
function showResponse(response) {
    $("#response").html("");
    $.each(response.items, function( index, value ) {
      $("#response").append("<li><a href='http://www.youtube.com/watch?v="+value.id.videoId+"'><img style='height:80px;width:120px;' src='"+value.snippet.thumbnails.default.url+"'>"+value.snippet.title+"</a></li>");
    });
}

// Called automatically when JavaScript client library is loaded.
function onClientLoad() {
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

// Called automatically when YouTube API interface is loaded (see line 9).
function onYouTubeApiLoad() {
    // This API key is intended for use only in this lesson.
    // See http://goo.gl/PdPA1 to get a key for your own applications.
    gapi.client.setApiKey('AIzaSyCR5In4DZaTP6IEZQ0r1JceuvluJRzQNLE');


}

function search(query) {
    // Use the JavaScript client library to create a search.list() API call.
    var request = gapi.client.youtube.search.list({
        part: 'snippet',
        q:query,
        maxResults:40,
        format:5
    });

    // Send the request to the API server,
    // and invoke onSearchRepsonse() with the response.
    request.execute(onSearchResponse);
}

// Called automatically with the response of the YouTube API request.
function onSearchResponse(response) {
    showResponse(response);
}


$("#search").blur(function(){
                    search($(this).val());
                });
                $("#search2").keyup(function(){
                    var query=$(this).val();
                    $.ajax({
                        type: "GET",
                        url: "http://suggestqueries.google.com/complete/search",
                        contentType: "application/json; charset=utf-8",
                        dataType: "jsonp",
                        data:{
                            "client":"youtube",
                            "ds":"yt",
                            "q":query
                        },
                        success: function(json){
                            $("#suggestions").html("");
                            $.each(json[1], function( index, value ) {
                              $("#suggestions").append("<li>"+value[0]+"</li>");
                            });
                        }
                    });
                });

/*
** PLAYER Javascript
*/

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
    playerVars:{
        controls:0,
        showinfo:0
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
  event.target.playVideo();
}

var done = false;
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 6000);
    done = true;
  }
}
function stopVideo() {
  player.stopVideo();
}
