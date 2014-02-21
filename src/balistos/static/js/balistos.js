/*global context_url, document, jQuery, Highcharts, console, alert */
/*jslint indent: 4, maxlen: 80 */

(function ($) {
    "use strict";
    $("form#login-form").on("submit",function(event){
        event.preventDefault();
        if($(this).find("input[name='login-username']").val().length<5 ||
         $(this).find("input[name='login-password']").val().length<5){
            $("#login-message").text("Your username or password is too short.").show();
            setTimeout(function(){$("#login-message").fadeOut(1000);},2000);
        }
        else{
            $(this).find("input[name='login-password']").val(hex_sha256($(this).find("input[name='login-password']").val()));
            var formdata=$(this).serialize();
            $.ajax({
                type: "POST",
                url: "/login",
                dataType:"json",
                data: formdata,
            }).done(function(response){
                if(response.error){
                    $("#login-message").text(response.error).show();
                    $("#login-form").find("input").val("");
                    setTimeout(function(){$("#login-message").fadeOut(1000);},2000);
                }
                else{
                    $("#login-navbar").html("You are logged in as <b>"+response.success+"</b>");
                    $("#create-playlist").slideDown(500);
                }
            });
        }
        $("#login-form").find("input").val("");
    });

    $("form#register-form").on("submit",function(event){
        event.preventDefault();
        if($(this).find("input[name='register-username']").val().length<5 ||
          $(this).find("input[name='register-password']").val().length<5){
            $("#register-message").text("Your username or password is too short.").show();
            setTimeout(function(){$("#register-message").fadeOut(1000);},2000);
        }
        else{
            if($(this).find("input[name='register-password']").val()==
            $(this).find("input[name='register-repeat']").val()){
                $(this).find("input[name='register-password']").val(hex_sha256($(this).find("input[name='register-password']").val()));
                $(this).find("input[name='register-repeat']").val("");
                var formdata=$(this).serialize();
                $.ajax({
                    type: "POST",
                    url: "/register",
                    dataType:"json",
                    data: formdata,
                }).done(function(response){
                    if(response.error){
                        $("#register-error").text(response.error).show();
                        setTimeout(function(){$("#register-message").fadeOut(1000);},2000);
                    }
                    else if(response.success){
                        setTimeout(function(){$("#register-message").fadeOut(1000);},2000);
                    }
                    else{
                        $("#register-dropdown").trigger("click");
                    }
                });
            }
            else{
                $("#register-message").text("Your passwords don't match.").show();
                setTimeout(function(){
                    $("#register-message").fadeOut(1000);
                },2000);
            }
        }
        $("#register-form").find("input").val("");
    });

}(jQuery));
