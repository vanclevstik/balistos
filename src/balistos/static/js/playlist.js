// we create Playlist Model.
function PlaylistModel(){
    var self=this;

    self.settings=ko.observableArray([
        {duration_limit:600}
    ]);
    self.videos=ko.observableArray([]);
    self.users=ko.observableArray([
        { username: "Bungle", type: "2"},
        { username: "George", type: "1"},
        { username: "Zippy", type: "0"}
    ]);

    self.messages=ko.observableArray([
        { author: "neykomir", time: "12:12",message:"ti si peder"},
        { author: "jerry", time: "12:32",message:"ti si tud peder"},
        { author: "vanč", time: "12:33",message:"ti si pa čist peder hoho"},
        { author: "lasč", time: "13:23",message:"ti si pa čist peder za čist"},
        { author: "košir", time: "14:13",message:"ti si pa čist peder nea"},
        { author: "jurc", time: "12:31",message:"ti si pa čist peder kaj ti je"},
        { author: "dasd", time: "12:31",message:"ti si pa čist peder tak"},
    ]);

    //function for adding videos to the array.
    self.addVideo=function(model,item){
        video=$(item.currentTarget);
        //we take data from the clicked result and insert it to array.
        videoarray={"title":video.attr('data-title'),
                    "image":video.attr('data-image'),
                    "id":video.attr('data-id')};
        //before sending the request, we inquire YouTube API for song duration.
        var request = gapi.client.youtube.videos.list({
            part: 'contentDetails',
            id:videoarray.id,
            type:'video',
        });

        // we send the request to the server with parameters
        request.execute(function(response){
            videoarray.duration=response.items[0].contentDetails.duration;
            $.ajax({
                type: "GET",
                url: "/playlist_add_video",
                dataType:"json",
                data: videoarray,
            }).done(function(data){
                self.sync();
            });
        });
        $("#response").hide();
        $("#search").val("");
    };

    //Function get total of users connected on current playlist.
    self.getUsersTotal=function(){
        return self.users().length;
    };

    //Function getSetting function help us get settings from model and simplify the call.
    self.getSetting=function(key){
        if(self.settings()[key])
            return self.settings()[key];
        else
            return false;
    };


    /* Each video has a button to delete a video. When user clicks on that
    button, we send a AJAX request with video_id as only argument. We expect no
    response. After the request is done, we sync the model. */
    self.removeFirstVideo=function(model,item){
        video=self.videos()[0].id();
        $.ajax({
            type: "GET",
            url: "/remove_video",
            dataType:"json",
            data: {video_id: video},
        }).done(function(data ){
            self.sync();
        });
    };

    /*Sync function is on the the main parts of the application. We call a
    AJAX request with no paramters and expect to recieve data for the whole
    model, which is videos, settings,user and messages.
    With videos we expect:
        title: title of the video
        id: youtube id of the video
        image: thumbnail image of vide
        likes: number of likes that video has recieved
        liked: the status of the like that current user made - 0 for neutral,
        1 for like and -1 for dislike
        owner: username of the user, who added it to queue
        start_time: where the video should start (only first in queue)
    settings:
        author: username of author
        time: time in format HH:mm:ss of when user posted message
        message: string containing message
    users:
        username: username of the user connected to playlist
        type: type of user - 0 for normal user , 1 for administrator
    settings:
        TODO
    */

    self.sync=function(){
        $.ajax({
            type: "GET",
            url: "/playlist_videos",
            dataType:"json",
        }).done(function(data){
            var mappedVideos=$.map(data.videos,function(item){
               return new Video(item);
            });
            self.videos(mappedVideos);
            self.settings(data.settings);
            var mappedUsers=$.map(data.users,function(item){
               return new User(item);
            });
            self.users(mappedUsers);

            var mappedMessages=$.map(data.messages,function(item){
               return new Message(item);
            });
            self.messages(mappedMessages);

        });

        $("#chat-div").scrollTop($("#chat-div")[0].scrollHeight);
    };

    /* we call sync function a period specified in miliseconds */
    self.syncInterval=function(period){
        self.sync();
        setTimeout(self.syncInterval(period),period);

    };
    self.syncInterval(2000);

    /*for easier access we compute some of the data for the first video*/
    self.firstVideoTitle=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].title();
        }
        else{
            return "Not yet chosen.";
        }
    },self);

    self.firstVideoId=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].id();
        }
        else{
            return false;
        }
    },self);

    self.firstVideoStart=ko.computed(function(){
        if(self.videos()[0]){
            return parseInt(self.videos()[0].start_time());
        }
        else
            return 0;
    },self);

}


function Video(data){
    this.title = ko.observable(data.title);
    this.id=ko.observable(data.id);
    this.image=ko.observable(data.image);
    this.likes=ko.observable(data.likes);
    this.liked=ko.observable(data.liked);
    this.owner=ko.observable(data.owner);
    this.start_time=ko.observable(data.start_time);

    /* for sending like, we simply send status of like along with id of video.*/
    this.addLike=function(){
        $.ajax({
            type: "GET",
            url: "/like_video",
            dataType:"json",
            data: {"video_id":this.id,
                   "like":1  //for like I will send 1, for unlike -1
                },
        }).done(function(data ){
            playlist.sync();
        });
    };

    this.removeLike=function(){
        $.ajax({
            type: "GET",
            url: "/like_video",
            dataType:"json",
            data: {"video_id":this.id,
                   "like":-1 //for like I will send 1, for unlike -1
            },
        }).done(function(data ){
            playlist.sync();
        });
    };

    /* to delete a video, we again send a simple AJAX request with video id. */
    this.removeVideo=function(model,item){
        $.ajax({
            type: "GET",
            url: "/remove_video",
            dataType:"json",
            data: {"video_id":this.id},
        }).done(function(data ){
            playlist.sync();
        });
        $("#response").hide();
        $("#search").val("");
    };
}

function User(data){
    this.username = ko.observable(data.username);
    //this.type=ko.observable(data.type);
    this.grantRights=function(model,item){
        $.ajax({
            type: "GET",
            url: "/grant_rights",
            dataType:"json",
            data: {
                "user_id":this.id
            },
        }).done(function(data ){
            playlist.sync();
        });
    };
}

function Message(data){
    this.author = ko.observable(data.author);
    this.time=ko.observable(data.time);
    this.message=ko.observable(data.message);
}


playlist=new PlaylistModel();
ko.applyBindings(playlist);
