/*jslint browser: true, this*/
/*global $, WOW, Cookies, gettext, blueimp, window*/

$(document).ready(function ($) {
    "use strict";

    // review modal
    $('#review-form-modal').on('show.bs.modal', function () {
        $(this).find('.modal-body').load('/review/create', function () {
            var form = $('#review-form'),
                button = $('#review-form-send');
            button.text(gettext('send'));
            button.unbind('click');
            button.click(function (event) {
                event.preventDefault();
                $('#review-form').find(':submit').click();
            });
            form.submit(function (event) {
                event.preventDefault();
                $.ajax({
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    success: function (response) {
                        $('#review-form-modal .modal-body').html(
                            '<span class="text-success">' + response.message + '</span>'
                        );
                        button.prop('disabled', false);
                        button.unbind('click');
                        button.text(gettext('close')).click(function (event) {
                            event.preventDefault();
                            $('#review-form-modal').modal('hide');
                        });
                    },
                    error: function () {
                        $('#review-form-modal .modal-body').html(
                            '<span class="text-danger">' +
                            gettext('Sorry! Error while sending message! Please refresh the page and try again') +
                            '</span>'
                        );
                    },
                    beforeSend: function () {
                        button.prop('disabled', true);
                    }
                });
            });
        });
    });

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

    // tooltip
    $('[data-toggle="tooltip"]').tooltip();

    //Notify defaults
    $.notifyDefaults({
        type: "success",
        placement: {
            from: "top",
            align: "center"
        }
    });

    (function () {
        var gallery = $('#gallery');
        if (!gallery.length) {
            return;
        }
        document.getElementById('gallery-photos').onclick = function (event) {
            event = event || window.event;
            var target = event.target || event.srcElement,
                link = target.src ? target.parentNode : target,
                options = {index: link, event: event},
                links = this.getElementsByTagName('a');
            blueimp.Gallery(links, options);
        };

        gallery.imagesLoaded(function () {
            $('#gallery-photos').wookmark({
                autoResize: true
            });
        });
    }());

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



