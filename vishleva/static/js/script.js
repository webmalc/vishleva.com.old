/*jslint browser: true, this*/
/*global $, WOW, Cookies, gettext*/

$(document).ready(function ($) {
    "use strict";

    // Ajax CSRFToken
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            var csrfSafeMethod = function (method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            };
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
            }
        }
    });

    //tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    //Notify defaults
    $.notifyDefaults({
        type: "success",
        placement: {
            from: "top",
            align: "center"
        }
    });

    //Send contact form
    var contactForm = $("#contact-form");
    contactForm.submit(function (e) {
        var button = $("#contact-form-button"),
            button_icon = $("#contact-form-button-icon");

        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/send_email",
            data: contactForm.serialize(),
            success: function (response) {
                button_icon.removeClass("fa-spinner fa-spin").addClass("fa-paper-plane")
                if (response.success) {
                    button.prop("disabled", false);
                    $.notify({
                        icon: "fa fa-check",
                        message: response.message
                    });
                } else {
                    $.notify({
                        icon: "fa fa-exclamation-triangle",
                        message: response.message
                    }, {type: "danger"});
                }
                contactForm.find("input[type=text], textarea").val("");
            },
            error: function () {
                $.notify({
                    icon: "fa fa-exclamation-triangle",
                    message: gettext('Sorry! Error while sending message! Please refresh the page and try again')
                }, {type: "danger"});
            },
            beforeSend: function () {
                button.prop("disabled", true);
                button_icon.removeClass("fa-paper-plane").addClass("fa-spinner fa-spin");
            }
        });
    });

    $(".scroll a, .navbar-brand, .gototop").click(function (event) {
        var target = $(this.hash);
        if (!target.length) {
            return;
        }
        event.preventDefault();
        $("html,body").animate({scrollTop: $(this.hash).offset().top - 50}, 600, "swing");
        $(".scroll li").removeClass("active");
        $(this).parents("li").toggleClass("active");
    });

    var wow = new WOW(
        {
            boxClass: "wowload",      // animated element css class (default is wow)
            animateClass: "animated", // animation css class (default is animated)
            offset: 0,          // distance to the element when triggering the animation (default is 0)
            mobile: true,       // trigger animations on mobile devices (default is true)
            live: true        // act on asynchronously loaded content (default is true)
        }
    );
    wow.init();

    $(".carousel").swipe({
        swipeLeft: function () {
            $(this).carousel("next");
        },
        swipeRight: function () {
            $(this).carousel("prev");
        },
        allowPageScroll: "vertical"
    });
});



