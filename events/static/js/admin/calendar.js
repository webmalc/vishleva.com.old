/*jslint browser: true, this*/
/*global $, window*/


$(document).ready(function () {
    "use strict";

    var link = function (end) {
            var begin = $('.calendar-select-begin'),
                beginDate = begin.attr('data-data'),
                beginTime = begin.attr('data-time'),
                endDate = end.attr('data-data'),
                endTime = end.attr('data-time');
            window.location = $('#events-calendar').attr('data-url')
                + '?begin_date=' + beginDate
                + '&begin_time=' + beginTime
                + '&end_date=' + endDate
                + '&end_time=' + endTime;
        },
        removeSelected = function () {
            if (!$('.calendar-select-begin').length) {
                return;
            }
            $('.calendar-select-begin .events-calendar-time').removeClass('display');
            $('.calendar-select-begin').removeClass('calendar-select-begin');
            $('#events-calendar a').click(function () {
                window.location = this.href;
            });
        };

    $('#events-calendar td').click(function () {

        if (!$('#events-calendar td.calendar-select-begin').length) {
            $(this).find('.events-calendar-time').addClass('display');
            $(this).addClass('calendar-select-begin');
            $('#events-calendar a').click(function (event) {
                event.preventDefault();
                link($(this).closest('td'));
            });
        } else if ($(this).hasClass('calendar-select-begin')) {
            removeSelected();
        } else {
            link($(this));
        }
    });
    $(document).keyup(function (e) {
        if (e.keyCode === 27) {
            removeSelected();
        }
    });
});