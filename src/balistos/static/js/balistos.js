/*global context_url, document, jQuery, Highcharts, console, alert */
/*jslint indent: 4, maxlen: 80 */

(function ($) {
    "use strict";
    $("form#login-form").on("submit",function(event){
        event.preventDefault();
        if($(this).find("input[name='login-username']").val().length<5 ||
         $(this).find("input[name='login-password']").val().length<5){
            $("#login-form").find("input").val("");
            $("#login-error").text("Your username or password is too short.").show();
            setTimeout(function(){$("#login-error").fadeOut(1000);},2000);
        }
        else{
            var formdata=$(this).serialize();
            $.ajax({
                type: "POST",
                url: "/login",
                dataType:"json",
                data: formdata,
            }).done(function(response){
                if(response.error){
                    $("#login-error").text(response.error).show();
                    $("#login-form").find("input").val("");
                    setTimeout(function(){$("#login-error").fadeOut(1000);},2000);

                }
                else{
                    $("#login-dropdown").trigger("click");
                }
            });
        }
    });

    $("form#register-form").on("submit",function(event){
        event.preventDefault();
        if($(this).find("input[name='register-username']").val().length<5 ||
         $(this).find("input[name='register-password']").val().length<5){
            $("#register-form").find("input").val("");
            $("#register-error").text("Your username or password is too short.").show();
            setTimeout(function(){$("#register-error").fadeOut(1000);},2000);
        }
        else{
            if($(this).find("input[name='register-password']").val()==
                $(this).find("input[name='register-repeat']").val()){
                var formdata=$(this).serialize();
                $.ajax({
                    type: "POST",
                    url: "/register",
                    dataType:"json",
                    data: formdata,
                }).done(function(response){
                    if(response.error){
                        $("#register-error").text(response.error).show();
                        $("#register-form").find("input").val("");
                        setTimeout(function(){$("#register-error").fadeOut(1000);},2000);
                    }
                    else{
                        $("#register-dropdown").trigger("click");
                    }
                });
            }
            else{
                $("#register-error").text("Your passwords don't match.").show();
                $("#register-form").find("input").val("");
                setTimeout(function(){
                    $("#register-error").fadeOut(1000);
                },2000);
            }
        }
    });

}(jQuery));
