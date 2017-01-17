/*jslint browser: true, this*/
/*global $, WOW, Cookies, gettext, blueimp, window, ace*/

/** Global admin object **/
var admin = {
    'aceEditor': function (textarea) {
        'use strict';

        if (!textarea.length) {
            return null;
        }
        var id = 'id_content_div' + textarea.prop('id');
        textarea.hide();
        textarea.after("<div id='" + id + "' style='width: 80%; height: 500px;'></div>");
        var editor = ace.edit(id);
        editor.setOptions({enableBasicAutocompletion: true});
        editor.getSession().setValue(textarea.val());
        editor.setTheme("ace/theme/monokai");
        editor.getSession().setMode("ace/mode/twig");
        editor.getSession().on("change", function () {
            textarea.val(editor.getSession().getValue());
        });

        return editor;
    }
};

$(document).ready(function ($) {
    "use strict";
    $('.sortedm2m-items a').click(function (event) {
        event.preventDefault();
        $(this).prev('input').trigger('click');
    });

    admin.aceEditor($('#gallery_form #id_description'));
    admin.aceEditor($('#gallery_form #id_extended-0-small_description'));
    admin.aceEditor($('#review_form #id_text'));

    $('.vTimeField').inputmask({mask: "99:99:99"});
    $('.vDateField').inputmask({mask: "9999-99-99"});

    /** datarange filter **/
    (function () {
        $('#changelist-filter input[type="reset"]').click(function (event) {
            event.preventDefault();
            var form = $(this).closest("form");
            form.attr('action', window.location.href);
            form.find('input[type="text"]').val('');
            form.submit();
        });
    }());

    /**
     * begin & end inputs
     */
    (function () {
        var begin = $('#id_begin_0'),
            end = $('#id_end_0');

        if (!begin.length || !end.length) {
            return;
        }

        begin.on('change, blur', function () {
            if (!end.val()) {
                end.val(begin.val());
            }
        });
    }());
});