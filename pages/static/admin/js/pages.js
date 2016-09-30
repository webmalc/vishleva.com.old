/*jslint browser: true*/
/*global $, ace*/
$(document).ready(function () {
    "use strict";
    var textarea = $("#id_content");
    textarea.hide();
    textarea.after("<div id='id_content_div' style='width: 80%; height: 500px;'></div>");
    var editor = ace.edit("id_content_div");
    editor.setOptions({enableBasicAutocompletion: true});
    editor.getSession().setValue(textarea.val());
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/twig");
    editor.getSession().on("change", function () {
        textarea.val(editor.getSession().getValue());
    });
});
