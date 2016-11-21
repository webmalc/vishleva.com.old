/*jslint browser: true, this*/
/*global $, WOW, Cookies, window*/

$(document).ready(function () {
    "use strict";

    $('.field-status:contains("not confirmed")').addClass('text-red');
    $('.field-status:contains("open")').addClass('text-green');
    $('.field-status:contains("closed")').addClass('text-muted');
});