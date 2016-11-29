/*jslint browser: true, this*/
/*global $, WOW, Cookies, window, gapi*/

var checkAuth = function () {
    'use strict';
    if (!$('#event_form').length && !$('.delete-confirmation').length) {
        return;
    }
    var calendarId = $('#id_google_calendar_id');

    var auth = function (immediate, callback) {
            gapi.auth.authorize(
                {
                    'client_id': '844817189895-a3eqkbt9va6hh1jqlm37s742gpnl8285.apps.googleusercontent.com',
                    'scope': 'https://www.googleapis.com/auth/calendar',
                    'immediate': immediate
                },
                callback
            );
        },
        deleteEvent = function (id, callback) {
            gapi.client.load('calendar', 'v3', function () {
                var request = gapi.client.calendar.events.delete({
                    'calendarId': 'primary',
                    'eventId': id
                });

                request.execute(callback);
                calendarId.val(null);
            });
        },
        createEvent = function (button) {
            var begin = $('#id_begin_0').val() + 'T' + $('#id_begin_1').val() + '+03:00',
                end = $('#id_end_0').val() + 'T' + $('#id_end_1').val() + '+03:00',
                title = $('#id_title').val(),
                description = $('#id_comment').val(),
                client = $('.field-client').find('strong a').html(),
                submitForm = function () {
                    button.off('click');
                    button.click();
                };

            if ($('#id_status').val() !== 'open' || Date.parse(begin) <= new Date()) {
                submitForm();
                return;
            }
            gapi.client.load('calendar', 'v3', function () {
                var event = {
                    'summary': title,
                    'description': description + '. ' + client,
                    'start': {
                        'dateTime': begin,
                        'timeZone': 'Europe/Moscow'
                    },
                    'end': {
                        'dateTime': end,
                        'timeZone': 'Europe/Moscow'
                    },
                    'reminders': {
                        'useDefault': false,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'email', 'minutes': 2 * 60},
                            {'method': 'popup', 'minutes': 60}
                        ]
                    }
                };

                var request = gapi.client.calendar.events.insert({
                    'calendarId': 'primary',
                    'resource': event
                });

                request.execute(function (event) {
                    if (event.id) {
                        calendarId.val(event.id);
                    }
                    submitForm();
                });
            });
        },
        addToCalendar = function () {
            if (window.location.hash && $('.delete-confirmation').length) {
                var hash = window.location.hash;
                $('.delete-confirmation input[type="submit"]').click(function (submit_delete_event) {
                    var button = $(this);
                    submit_delete_event.preventDefault();
                    deleteEvent(hash.substring(1), function () {
                        button.off('click');
                        button.click();
                        return;
                    });
                });
                return;
            }

            if (calendarId.val()) {
                gapi.client.load('calendar', 'v3', function () {
                    var request = gapi.client.calendar.events.get({
                        'calendarId': 'primary',
                        'eventId': calendarId.val()
                    });

                    request.execute(function (event) {
                        if (event.id) {
                            var linkText = event.status !== 'cancelled'
                                ? 'open in google calendar'
                                : 'CANCELLED';
                            $('.field-google_calendar_id .help')
                                .append(' - <a href="' + event.htmlLink + '" target="_blank">' + linkText + '</a>');
                        }
                    });
                });

                $('.deletelink').attr('href', $('.deletelink').attr('href') + '#' + calendarId.val());
            }

            $('#event_form input[type="submit"]').click(function (submit_event) {
                submit_event.preventDefault();
                var button = $(this);

                if (!calendarId.val()) {
                    createEvent(button);
                } else {
                    deleteEvent(calendarId.val(), function (event) {
                        createEvent(button);
                    });
                }
            });
        },
        authPopup = function (authResult) {
            if (authResult && !authResult.error) {
                addToCalendar();
                return;
            }
            $('#event_form input[type="submit"]').click(function (event) {
                event.preventDefault();
                auth(false, authPopup);
            });
        };
    auth(true, authPopup);
};

$(document).ready(function () {
    "use strict";

    $('.field-status:contains("not confirmed")').addClass('text-red');
    $('.field-status:contains("open")').addClass('text-green');
    $('.field-status:contains("closed")').addClass('text-muted');
});