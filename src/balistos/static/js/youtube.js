// Your use of the YouTube API must comply with the Terms of Service:
// https://developers.google.com/youtube/terms

function onClientLoad() {
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

function onYouTubeApiLoad() {
    gapi.client.setApiKey('AIzaSyCR5In4DZaTP6IEZQ0r1JceuvluJRzQNLE');
}

function search(query) {
    var request = gapi.client.youtube.search.list({
        part: 'snippet',
        q:query,
        type:'video',
        maxResults:8,
        format:5
    });
    request.execute(onSearchResponse);
}

function onSearchResponse(response) {
    $("#response").html("");
    $.each(response.items, function( index, value ) {

      $("#response").append("<li data-title='"+value.snippet.title+"' data-image='"+value.snippet.thumbnails.default.url+"' title='Add "+value.snippet.title+" to playlist' data-bind='click: addVideo' data-id='"+value.id.videoId+"' id='video-"+value.id.videoId+"'><img src='"+value.snippet.thumbnails.default.url+"'><div class='title'>"+value.snippet.title+"</div></li>");
       ko.applyBindings(playlist, $("#video-"+value.id.videoId)[0]);
        
    });
    $("#response").show();
}

/*
** PLAYER Javascript
*/

var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


var player;
function onYouTubeIframeAPIReady() {
    var video=$("#video-id").text();
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: video,
        playerVars:{
            controls:0,
            showinfo:0,
            wmode:'transparent',
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
