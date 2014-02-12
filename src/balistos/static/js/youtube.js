// Your use of the YouTube API must comply with the Terms of Service:
// https://developers.google.com/youtube/terms

// showResponse(response) is triggered from search function and updates #response ul container with results */
function showResponse(response) {
    $("#response").html("");
    $.each(response.items, function( index, value ) {
        $("#response").append("<li data-title='"+value.snippet.title+"' data-image='"+value.snippet.thumbnails.default.url+"' title='Add "+value.snippet.title+" to playlist' data-bind='click: addVideo' data-id='"+value.id.videoId+"' id='video-"+value.id.videoId+"'><img src='"+value.snippet.thumbnails.default.url+"'><div class='title'>"+value.snippet.title+"</div></li>");
        ko.applyBindings(playlist, $("#video-"+value.id.videoId)[0]);
    });
    $("#response").show();
}

// onClientLoad() is called externally when Youtube API is loaded.
function onClientLoad() {
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

// onYouTubeApiLoad() is called externally when Youtube API is loaded.
function onYouTubeApiLoad() {
    gapi.client.setApiKey('AIzaSyCnR3Vv-Erxjaa-IJapIXCnvgTOuXLXItA');
}

//search(query) takes a string query and searches Youtube Data Api for results. It returns 8 hits with only videos which are embeedable.
function search(query) {

    var request = gapi.client.youtube.search.list({
        part: 'snippet',
        q:query,
        type:'video',
        maxResults:8,
        format:5,
        key:'AIzaSyCnR3Vv-Erxjaa-IJapIXCnvgTOuXLXItA'
    });
    request.execute(showResponse);
}


// we inject YouTube API library into our page 
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;

// we wait for YouTube API to completely load and then assign listeners for events.
function onYouTubeIframeAPIReady() {

    // when user types a query into search bar, we invoke search method to return results.
    $("#search").keyup(function(e){
        if($(this).val()===""){
            $("#response").hide();
        }
        else{
            var code = (e.keyCode ? e.keyCode : e.which);
            var idx;
            if (code == 40) {
                if($("#response").children("li.active").length<1){
                    $("#response").children("li:first-child").addClass("active");
                }
                else{
                    idx=$("#response").children("li.active").index()+1;
                    $("#response").children().removeClass("active");
                    if(idx>7)
                        idx=0;
                    $("#response").children().eq(idx).addClass("active");
                }
            } 
            else if (code == 38) {
                if($("#response").children("li.active").length<1){
                    $("#response").children().eq(7).addClass("active");
                }
                else{
                    idx=$("#response").children("li.active").index()-1;
                    $("#response").children().removeClass("active");
                    if(idx<0)
                        idx=7;
                    $("#response").children().eq(idx).addClass("active");
                }
            }
            else if (code == 13) {
                if($("#response").children("li.active").length>0){
                    $("#response").children("li.active").trigger("click");
                }
                
            }
            else{
                search($(this).val());
            }
            
        }
    });

    // we listen to #video-id div, which is dinamically linked to last video id and on change played video. If it was empty before, we first initialize the player.
    $('#video-id').bind("DOMSubtreeModified",function(){
        if($(this).text()!==""){
            if(player){
                player.loadVideoById($(this).text(),0, "large");
            }
            else{
                initPlayer();
            }
        }
    });

    initPlayer();

}

function initPlayer(){
    // initialization of the YouTube IFrame API player. If there is no clip in playlist, we instead write a message.
    var video=$("#video-id").text();
    var start=parseInt($("#video-start").text());
    if(video!==""){
        player = new YT.Player('player', {
            height: '390',
            width: '640',
            videoId: video,
            playerVars:{
                controls:0,
                showinfo:0,
                start:start,
                disablekb:1,
                wmode:'transparent',
            },
            events: {
                'onReady': onPlayerReady
            }
        });
    }
    else{
        $("#player").text("No video currently in the queue.");
    }
}

// when player is initialized, we automatically play the video.
function onPlayerReady(event) {
    event.target.playVideo();
}
