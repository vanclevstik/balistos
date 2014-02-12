// we create Playlist Model.
function PlaylistModel(){
    var self=this;
    self.videos=ko.observableArray([]);

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

        // we send the request to the server with parameters id,title,image and duration
        request.execute(function(response){
            videoarray.duration=response.items[0].contentDetails.duration;
            $.ajax({
                type: "GET",
                url: "/playlist_add_video",
                dataType:"json",
                data: videoarray,
            }).done(function(data ){
                //after recieving response, we sychronise the playlist data
                var mappedVideos=$.map(data,function(item){ return new Video(item);});
                self.videos(mappedVideos);
            });
        });
        $("#response").hide();
        $("#search").val("");
    };

    self.removeVideo=function(model,item){
        video=$(item.currentTarget);
        $.ajax({
            type: "GET",
            url: "/playlist_add_video",
            dataType:"json",
            data: video.id,
        }).done(function(data ){
            //after recieving response, we sychronise the playlist data
            var mappedVideos=$.map(data,function(item){ return new Video(item);});
            self.videos(mappedVideos);
        });
    };

    $.ajax({
        type: "GET",
        url: "/playlist_videos",
        dataType:"json",
    }).done(function(data){
        var mappedVideos=$.map(data,function(item){ return new Video(item);});
        self.videos(mappedVideos);
    });



    self.firstVideoTitle=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].title();
        }
        else{
            return "Not yet chosen";
        }
    },self);

    self.secondVideoTitle=ko.computed(function(){
        if(self.videos()[1]){
            return self.videos()[1].title();
        }
        else{
            return "Not yet chosen";
        }
    },self);

    self.firstVideoId=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].id();
        }
    },self);

    self.firstVideoStart=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].start_time();
        }
        else
            return 0;
    },self);

    self.sync=function(){
        $.ajax({
            type: "GET",
            url: "/playlist_videos",
            dataType:"json",
        }).done(function(data){
            var mappedVideos=$.map(data,function(item){ return new Video(item);});
            self.videos(mappedVideos);
            setTimeout(self.sync,2000);
        });
    };
    self.sync();
}


function Video(data){
    this.title = ko.observable(data.title);
    this.id=ko.observable(data.id);
    this.image=ko.observable(data.image);
    this.likes=ko.observable(data.likes);
    this.start_time=ko.observable(data.start_time);

    this.addLike=function(){
        $.ajax({
            type: "GET",
            url: "/like_video",
            dataType:"json",
            data: {"videoid":this.id,
                   "like":1  //for like I will send 1, for unlike -1
                },
        }).done(function(data ){
            var likes=this.likes();
            this.likes(likes+1);
        });
    };


    this.removeLike=function(){
        $.ajax({
            type: "GET",
            url: "/unlike_video",
            dataType:"json",
            data: {"videoid":this.id,
                   "like":-1 //for like I will send 1, for unlike -1
            },
        }).done(function(data ){
            var likes=this.likes();
            this.likes(likes-1);
        });
    };
}

playlist=new PlaylistModel();
ko.applyBindings(playlist);
