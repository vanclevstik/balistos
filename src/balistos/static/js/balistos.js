/*global context_url, document, jQuery, Highcharts, console, alert */
/*jslint indent: 4, maxlen: 80 */

(function ($) {
    "use strict";

    //when user clicks on hide player, we destroy the Embeeded player and show
    //the button to bring it back
    $("#hide-player").click(function(){
        $(this).hide();
        $(".player").hide();
        $("#show-player").show();
        if(player){
            player.destroy();
            player=null;
        }
    });

    /* When user clicks on show player, we initialize it again at the correct
    point and show it to user along with hide button. */
    $("#show-player").click(function(){
        $(this).hide();
        $(".player").fadeIn();
        $("#hide-player").show();
        initPlayer();

    });

    /* We catch when user clicks outside of search playlist result area and
    hide the results so it acts as a normal select element. */
    $(document).click(function(){
        $('#response-playlist').hide();
    });
    $(document).on("click","#response-playlist",function(event){
        event.stopPropagation();
    });

    /* When user want to visit a protected playlist, we ask him to provide
    password. */
    $(document).on("click",".protected_playlist",function(event){
        event.preventDefault();
        $(this).parents("li").find("form").fadeToggle();
    });

    /*
    When user enters password for protected playlist we send an ajax form
    to validate it and if request sends us success message we redirect user
    on correct address of the playlist
    arguments:
        -uri: unique identifier of target playlist
        -password: password of target playlist
    */

    $(document).on("submit",".protected_playlist_form",function(event){
        var uri=$(this).find("input").attr("data-uri");
        var item=$(this).parents("li");
        event.preventDefault();
        $.ajax({
            type: "GET",
            url: "/authenticate_playlist",
            dataType:"json",
            data:{
                "password":$(this).find("input").val(),
                "uri":uri
            }
        }).done(function(data){
            if(data.success){
                window.location.href="/playlist/"+uri;
            }
            else if(error){
                item.find(".playlist_password_error").text(data.error);
            }
        });
    });

    /* When user types a string in the playlist search input, we call AJAX
    request, which returns us the results with title and descripton and if
    playlist is protected.
    arguments:
        -query: search query string
    response:
        -title: title of the playlist
        -uri: unique identifier of playlist eg. best_playlist
        -description: short description of playlist
    */
    $("#search_playlist").keyup(function(){
        $.ajax({
            type: "GET",
            url: "/search_playlists",
            dataType:"json",
            data:{
                "query":$(this).val()
            }
        }).done(function(data){
            if(data.length<1){
                $("#response-playlist").html('No results for this query...');
                $("#response-playlist").show();
            }
            else{
                $("#response-playlist").html("");
                $.each(data, function( index, value ) {
                    $("#response-playlist").append('<a href="'+
                    '/playlist/'+value.uri+'"><div class="title">'+
                    value.title+'</div><div class="'+
                    'description">'+value.description+'</div></a>');
                });
                $("#response-playlist").show();
            }
        });
    });

    /* Standard login form with AJAX. We first if your username and password are
    at least 5 characters long and for 2 seconds display an error message. If
    they are both ok, we send the request to server and on error display that
    error, but on success change the button and enable all the functionality
    of the webpage. Password is hashed with sha256 before being sent to server.
    argumnents:
        -login-username
        -login-password
    response:
        error: error message on failed attemp
        success: on successful attemp we recieve username
    */

    $("#login-form").on("submit",function(event){
        $("#login-form input").removeClass("red");
        $("#login-form .error").text("");
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/login",
            dataType:"json",
            data:{
                "login-username": $(this)
                    .find("#login-username").val(),
                "login-password": hex_sha256($(this)
                    .find("#login-password").val())
            },
        }).done(function(response){
            if(response.error){
                $("#login-username-error").text(response.error).show();
                $("#login-form input").addClass("red");
                $("#login-password").val("");
            }
            else{
                window.location.reload();
            }
        });

    });

    /* Standard registration form that works the same way as login form. We
    also validate email address and check on password matching on client side.
    arguments:
        -register-username
        -register-password
        -register-email
    response:
        -error: error message on failed attemp or
        -success: on successful attemp we recieve username
    */

    $("#register-form").on("submit",function(event){
        event.preventDefault();
        $("#register-form input").removeClass("red");
        $("#register-form .error").text("");

        if($(this).find("input[name='register-password']").val().length<5){
            $("#registration-password-error")
                .text("Your password is too short.");
            $("#register-password").addClass("red");
            $("#register-form").find("input[type='password']").val("");
        }
        else if($(this).find("input[name='register-username']").val().length<5){
            $("#registration-username-error")
                .text("Your username is too short.");
            $("#register-username").addClass("red");
        }
        else if(!validateEmail($(this).find("input[name='register-email']")
            .val())){
            $("#registration-email-error")
                .text("Your email is not valid.");
            $("#register-email").addClass("red");
        }
        else{
            if($(this).find("#register-password").val()==
                $(this).find("#register-repeat").val()){
                $.ajax({
                    type: "POST",
                    url: "/register",
                    dataType:"json",
                    data:{
                        "register-username": $(this)
                            .find("#register-username").val(),
                        "register-password":
            hex_sha256($(this).find("#register-password").val()),
                        "register-email": $(this).
                            find("#register-email").val(),
                    },
                }).done(function(response){
                    if(response.error){
                        $("#registration-email-error")
                        .text(response.error);
                        $("#register-email").addClass("red");
                    }
                    else{
                        window.location.reload();
                    }
                });
            }
            else{
                $("#registration-repeat-error")
                .text("Passwords don't match.");
                $("#register-repeat").addClass("red");
                $("#register-form").find("input[type='password']").val("");
            }
        }

    });

    /* Simple chat AJAX request that sends a short message to server to be
    included in chat at current playlist.
    arguments:
        -message: short message string
    response:
        we don't expect any response, user will se his message when page syncs
        again
    */
    $("#chat-form").submit(function(){
        $.ajax({
            type: "POST",
            url: "/chat_message",
            dataType:"json",
            data: $(this).serialize(),
        }).done(function(data ){
            playlist.sync();
        });
        $(this).find("textarea").val("");
        return false;
    });

    /* we allow users to submit chat message with only enter key */
    $("#chat-message").keydown(function (event) {
        var keypressed = event.keyCode || event.which;
        if (keypressed == 13) {
            event.preventDefault();
            $("#chat-form").submit();
        }
    });

    /* controls for volume slider. We use a simple plugin, which we first
    initialize, then create a listener which sets player's volume according to
    sliders value. */
    $("#volume-slider").simpleSlider();
    $("#volume-slider").bind("slider:changed", function (event, data) {
        if(player){
            player.setVolume(parseInt(data.value*100));
        }
    });

    /* clicking on speaker icon mutes the player by setting the volume to 0. */
    $(".speaker").click(function(){
        $("#volume-slider").simpleSlider("setValue",0);
        if(player){
            player.setVolume(0);
        }
    });

    /* email validation function for front-end email verification. */
    function validateEmail(email){
        return /^.+@.+\..+$/.test(email);
    }

    /* on create playlist
    $("#password_check").change(function(){
        $("#playlist_password").fadeToggle();
    });



    /* dropdown menu for the login authentication functionality. */
    $(".user").click(function(e){
        e.stopPropagation();
        $("#logout").slideDown();
    });
    $(".open-login").click(function(e){
        e.stopPropagation();
        $(".menu-button").removeClass("active");
        $(".open-login").addClass("active");
        $(".dropdown").hide();
        $("#login").slideDown();
    });
    $(".open-register").click(function(e){
        e.stopPropagation();
        $(".menu-button").removeClass("active");
        $(".open-register").addClass("active");
        $(".dropdown").hide();
        $("#register").slideDown();
    });
    $(".open-create").click(function(e){
        e.stopPropagation();
        $(".menu-button").removeClass("active");
        $(".open-register").addClass("active");
        $(".dropdown").hide();
        $("#create").slideDown();
    });
    $(".dropdown").click(function(e){
        e.stopPropagation();
    });
    $(document).click(function(){
        $(".menu-button").removeClass("active");
        $(".dropdown").hide();
    });


    /* actions of share icons, which open new popup window with appropriate share interface */
    $(".share-icon.facebook").click(function(){
        window.open('http://www.facebook.com/sharer.php?u='+$(location).attr('href'),encodeURI($(document).attr('title')),'width=600,height=300');
    });
    $(".share-icon.twitter").click(function(){
        window.open('http://twitter.com/home?status='+$(location).attr('href')+'+'+encodeURI($(document).attr('title')), $(location).attr('href'), 'width=600,height=300');
    });
    $(".share-icon.google").click(function(){
        window.open('https://plus.google.com/share?url='+$(location).attr('href'), encodeURI($(document).attr('title')), 'width=600,height=300');
    });



}(jQuery));
