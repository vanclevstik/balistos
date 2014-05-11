// Your use of the YouTube API must comply with the Terms of Service:
// https://developers.google.com/youtube/terms

//catch click on anywhere except results of search and hide the results
$(document).click(function(){
    $('#response').hide();
 });
$(document).on("click","#response",function(event){
    event.stopPropagation();
});

// showResponse(response) is triggered from search function and updates #response ul container with results */
function showResponse(response) {
    $("#response").html("");
    $.each(response.items, function( index, value ) {
        $("#response").append('<li data-title="'+value.snippet.title.replace("'","\'")+
        '" data-image="'+value.snippet.thumbnails.default.url+'"" title="Add '+
        value.snippet.title+' to playlist" data-bind="click: addVideo" data-id="'+
        value.id.videoId+'" id="video-'+value.id.videoId+'"><img src="'+
        value.snippet.thumbnails.default.url+'"><div class="title">'+
        value.snippet.title+'</div></li>');

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

//search(query) takes a string query and searches Youtube Data Api for results.
//It returns 8 hits with only videos which are embeedable.
function search(query) {
    var request = gapi.client.youtube.search.list({
        part: 'snippet',
        q:query,
        type:'video',
        maxResults:12,
        format:5,
        videoEmbeddable:true,
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
    $("#search").click(function(){
        $("#response").show();
    });
    $("#search").keyup(function(e){
        //if query is empty we hide the results
        if($(this).val()===""){
            $("#response").hide();
        }
        else{
            //we check if user clicks down, up and enter to bind the keys
            var code = (e.keyCode ? e.keyCode : e.which);
            var idx;

            if (code == 40) {
                if($("#response").children("li.active").length<1){
                    $("#response").children("li:first-child").addClass("active");
                }
                else{
                    idx=$("#response").children("li.active").index()+1;
                    $("#response").children().removeClass("active");
                    if(idx>19){
                        idx=0;
                        $(".autocomplete").scrollTop(0);
                    }
                    if (idx>9){
                        $(".autocomplete").scrollTop(((parseInt(idx)-9)*42));
                    }
                    $("#response").children().eq(idx).addClass("active");
                }
            }
            else if (code == 38) {
                if($("#response").children("li.active").length<1){
                    $("#response").children().eq(19).addClass("active");
                    $(".autocomplete").scrollTop(420);
                }
                else{
                    idx=$("#response").children("li.active").index()-1;
                    $("#response").children().removeClass("active");
                    if(idx<0){
                        idx=19;
                        $(".autocomplete").scrollTop(420);
                    }
                    if (idx<10){
                        $(".autocomplete").scrollTop(((parseInt(idx))*42));
                    }
                    $("#response").children().eq(idx).addClass("active");
                }
            }
            else if (code == 13) {
                if($("#response").children("li.active").length>0){
                    $("#response").children("li.active").trigger("click");
                }
                
            }
            else{
                delaySearch($(this).val());
            }
            
        }
    });

    /* user can mute and unmute video by clicking on big overlay on player */
    $(document).on("click",".overlay.mute",function(){
        player.mute();
        $(".overlay").removeClass("mute").addClass("unmute");
    });

    $(document).on("click",".overlay.unmute",function(){
        player.unMute();
        $(".overlay").removeClass("unmute").addClass("mute");
    });
    
    /* we listen to #video-id div, which is dinamically linked to last video 
    id and on change played video. If it was empty before, we first initialize
    the player. */
    $("#video-id").bind("DOMSubtreeModified",function(){
        if($(this).text()!==""){
            if(player){
                player.loadVideoById(playlist.firstVideoId(),0, "large");
                $("title").text("Balistos - "+playlist.firstVideoTitle());
            }
            else{
                initPlayer();
            }
        }
    });
    initPlayer();
}

/* when page loads or user shows a player we initialize YouTube IFrame API
player. We first check whether it's already initialized and then check if
we have managed to retrieve video and it's start time from the server. In
options we disable all visible controls and keyboard controls. We hide all the
information and user annotations. We make video start at time specified by the
server */

function initPlayer(){
    if(!player){
        if(playlist.firstVideoId() && playlist.firstVideoStart()){
            $("title").text("Balistos - "+playlist.firstVideoTitle());
            player = new YT.Player("player", {
                height: "390",
                width: "640",
                videoId: playlist.firstVideoId(),
                playerVars:{
                    controls:0,
                    showinfo:0,
                    start:parseInt(playlist.firstVideoStart()),
                    disablekb:1,
                    iv_load_policy:3,
                    wmode:"transparent",
                    rel:0
                },
                events: {
                    "onReady": onPlayerReady
                }
            });
        }
        else{
            $("#player").text("No video currently in the queue.");
            setTimeout(initPlayer,500);
        }
    }
}

/* this function takes care of progress bar at the bottom of player. It gets 
data from player object and assignes css properties that reflect it. This 
function is called every second. */
function updateProgress(){
    var percent=player.getCurrentTime()/player.getDuration()*100;
    $(".progress .bar").width(percent+"%");
    $(".elapsed").text(convertToTime(player.getCurrentTime()));
    $(".total").text(" / "+convertToTime(player.getDuration()));
    setTimeout(updateProgress,1000);
}

/* this function converts seconds to formatted time mm:ss */
function convertToTime(seconds){
    var minutes=parseInt(seconds/60);
    seconds=parseInt(seconds%60);
    if (seconds<10)
        seconds="0"+seconds;
    
    return minutes+":"+seconds;
}

/* when player is initialized, we automatically play the video and initialize
progress bar.*/
function onPlayerReady(event) {
    event.target.playVideo();
    updateProgress();
}

//Detect keystroke and only execute after the user has finish typing (waits 0.3s)
var typingTimer;
var doneTypingInterval =300;
function delaySearch(query){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(function(){search(query);},doneTypingInterval);
    return true;
}
