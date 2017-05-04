/* global tinymce */
/** Global admin object **/
var admin = {
    aceEditor: function(textarea) {
        'use strict';

        if (!textarea.length) {
            return null;
        }
        var id = 'id_content_div' + textarea.prop('id');
        textarea.hide();
        textarea.after("<div id='" + id + "' style='width: 80%; height: 500px;'></div>");
        var editor = ace.edit(id);
        editor.setOptions({
            enableBasicAutocompletion: true,
        });
        editor.getSession().setValue(textarea.val());
        editor.setTheme('ace/theme/monokai');
        editor.getSession().setMode('ace/mode/twig');
        editor.getSession().on('change', function() {
            textarea.val(editor.getSession().getValue());
        });
        return editor;
    },
    tinymce: function(selector) {
        tinymce.init({
            selector: selector,
            height: 500,
            theme: 'modern',
            forced_root_block: false,
            plugins: [
                'advlist autolink lists link image charmap print preview hr anchor pagebreak',
                'searchreplace wordcount visualblocks visualchars code fullscreen',
                'insertdatetime media nonbreaking save table contextmenu directionality',
                'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc spellchecker'
            ],
            toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
            toolbar2: 'print preview media | forecolor backcolor emoticons | codesample spellchecker',
            spellchecker_languages: "Russian=ru,Ukrainian=uk,English=en",
            spellchecker_language: "ru",  // default language
            spellchecker_rpc_url: "http://speller.yandex.net/services/tinyspell",
            image_advtab: true
        });
    },
};

$(document).ready(function($) {
    'use strict';
    $('.sortedm2m-items a').click(function(event) {
        event.preventDefault();
        $(this).prev('input').trigger('click');
    });

    admin.tinymce(
        '#gallery_form #id_description, #gallery_form #id_extended-0-small_description, #review_form #id_text'
    );
     
    $('.vTimeField').inputmask({
        mask: '99:99:99',
    });
    $('.vDateField').inputmask({
        mask: '9999-99-99',
    });

    /** datarange filter **/
    (function() {
        $('#changelist-filter input[type="reset"]').click(function(event) {
            event.preventDefault();
            var form = $(this).closest('form');
            form.attr('action', window.location.href);
            form.find('input[type="text"]').val('');
            form.submit();
        });
    }());

    /**
     * begin & end inputs
     */
    (function() {
        var begin = $('#id_begin_0'),
            end = $('#id_end_0');

        if (!begin.length || !end.length) {
            return;
        }

        begin.on('change, blur', function() {
            if (!end.val()) {
                end.val(begin.val());
            }
        });
    }());

    // admin filter select
    (function() {
        $('.admin-filter-select').change(function() {
            window.location.href =  $(this).val();
        });
    }());
});
