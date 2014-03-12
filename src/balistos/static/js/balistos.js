/*global context_url, document, jQuery, Highcharts, console, alert */
/*jslint indent: 4, maxlen: 80 */

(function ($) {
    "use strict";

    //when user clicks on hide player, we destroy the Embeeded player and show
    //the button to bring it back
    $("#hide-player").click(function(){
        $(this).hide();
        $(".player").hide();
        player.destroy();
        player=null;
        $("#show-player").fadeIn();
    });

    /* When user clicks on show player, we initialize it again at the correct
    point and show it to user along with hide button. */
    $("#show-player").click(function(){
        $(this).hide();
        initPlayer();
        $(".player").fadeIn();
        $("#hide-player").fadeIn();
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
        -protected: boolean which say whether playlist is password protected
        -description: short description of playlist
    */
    $("#search-playlist").keyup(function(){
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
                    if(value.protected){
                        $("#response-playlist").append('<li><a href="'+
                        '/playlist/'+value.uri+'" class="protected_playlist">'+
                        value.title+'</a><form class="protected_playlist_form"'+
                        'style="display:none"><input data-uri="'+value.uri+
                        '" type="text" class="form-control" placeholder="Enter'+
                        'playlist password" /><button type="submit">Join'+
                        '</button></form><div class="playlist_password_error">'+
                        '</div></li>');
                    }
                    else{
                        $("#response-playlist").append('<li><a href="'+
                        '/playlist/'+value.uri+'">'+value.title+'</a></li>');
                    }
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

    $("form#login-form").on("submit",function(event){
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/login",
            dataType:"json",
            data:{
                "login-username": $(this)
                    .find("input[name='login-username']").val(),
                "login-password": hex_sha256($(this)
                    .find("input[name='login-password']").val())
            },
        }).done(function(response){
            if(response.error){
                $("#login-message").text(response.error).show();
                $("#login-form").find("input").val("");
                setTimeout(function(){
                    $("#login-message").fadeOut(1000);
                },2000);
            }
            else{
                $("#username-string").text(response.success);
                $(".not-logged-in").hide();
                $("#hidden-search").hide();
                $("#search").fadeIn(1000);
                $(".logged-in").fadeIn(1000);
                $.ajax({
                    type: "GET",
                    url: "/latest_playlists",
                    dataType:"json",
                });
            }
        });
        $("#login-form").find("input[type='password']").val("");
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

    $("form#register-form").on("submit",function(event){
        event.preventDefault();
        if($(this).find("input[name='register-username']").val().length<5 ||
          $(this).find("input[name='register-password']").val().length<5){
            $("#register-message")
                .text("Your username or password is too short.")
                .show();
            setTimeout(function(){
                $("#register-message").fadeOut(1000);
            },2000);
        }
        else if(!validateEmail($(this).find("input[name='register-email']")
            .val())){
            $("#register-message")
                .text("You have entered invalid email adress.")
                .show();
            setTimeout(function(){
                $("#register-message").fadeOut(1000);
            },2000);
        }
        else{
            if($(this).find("input[name='register-password']").val()==
            $(this).find("input[name='register-repeat']").val()){
                $(this).find("input[name='register-repeat']").val("");
                $.ajax({
                    type: "POST",
                    url: "/register",
                    dataType:"json",
                    data:{
                        "register-username": $(this)
                            .find("input[name='register-username']").val(),
                        "register-password":
            hex_sha256($(this).find("input[name='register-password']").val()),
                        "register-email": $(this).
                            find("input[name='register-email']").val(),
                    },
                }).done(function(response){
                    if(response.error){
                        $("#login-message").text(response.error).show();
                        $("#login-form").find("input").val("");
                        setTimeout(function(){
                            $("#login-message").fadeOut(1000);
                        },2000);
                    }
                    else{
                        $("#username-string").text(response.success);
                        $(".not-logged-in").hide();
                        $("#hidden-search").hide();
                        $("#search").fadeIn(1000);
                        $(".logged-in").fadeIn(1000);
                    }
                });
            }
            else{
                $("#register-message")
                    .text("Your passwords don't match.")
                    .show();
                setTimeout(function(){
                    $("#register-message").fadeOut(1000);
                },2000);
            }
        }
        $("#register-form").find("input[type='password']").val("");
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
        $(this).find("input").val("");
        return false;
    });

    $("#password_check").change(function(){
        $("#playlist_password").fadeToggle();
    });


    function validateEmail(email){
        return /^.+@.+\..+$/.test(email);
    }
}(jQuery));
