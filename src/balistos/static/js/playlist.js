function PlaylistModel(){
    var self=this;
    self.videos=ko.observableArray([]);

    var mappedVideos=$.map(videoarray,function(item){ return new Video(item);});
    self.videos(mappedVideos);


    self.addVideo=function(model,item){
        video=$(item.currentTarget);
        self.videos.push(new Video({title:video.attr('data-title'),image:video.attr('data-image'),id:video.attr('data-id'),likes:0}));
        $("#response").hide();
    };
}


function Video(data){
    this.title = ko.observable(data.title);
    this.id=ko.observable(data.id);
    this.image=ko.observable(data.image);
    this.likes=ko.observable(data.likes);

    this.addLike=function(){
        var likes=this.likes();
        this.likes(likes+1);
    };
}


playlist=new PlaylistModel();

ko.applyBindings(playlist);