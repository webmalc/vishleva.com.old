/*jslint browser: true, this*/
/*global $, WOW, Cookies, gettext, blueimp, window*/

$(document).ready(function ($) {
    "use strict";
    $('.sortedm2m-items a').click(function (event) {
        event.preventDefault();
        $(this).prev('input').trigger('click');
    });
});