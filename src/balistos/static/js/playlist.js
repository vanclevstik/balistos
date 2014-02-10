function PlaylistModel(){
    var self=this;
    self.videos=ko.observableArray([]);

    self.addVideo=function(model,item){
        video=$(item.currentTarget);
        videoarray={"title":video.attr('data-title'),
                    "image":video.attr('data-image'),
                    "id":video.attr('data-id')};

        var request = gapi.client.youtube.videos.list({
            part: 'contentDetails',
            id:videoarray.id,
            type:'video',
        });

        request.execute(function(response){
            videoarray.duration=response.items[0].contentDetails.duration;
            $.ajax({
                type: "GET",
                url: "/playlist_add_video",
                dataType:"json",
                data: videoarray,
            }).done(function(data ){
                var mappedVideos=$.map(data,function(item){ return new Video(item);});
                self.videos(mappedVideos);
            });
        });

        // self.videos.push(new Video({title:video.attr('data-title'),image:video.attr('data-image'),id:video.attr('data-id'),likes:0}));
        $("#response").hide();
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
    },self);

    self.firstVideoId=ko.computed(function(){
        if(self.videos()[0]){
            return self.videos()[0].id();
        }
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
