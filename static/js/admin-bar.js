var id_fields_news = {'title': 20, 'subtitle': 110, 'body': 250 }
var id_fields_novel = {'title': 250, 'subtitle': 250, 'body': 10000 }
var id_fields_story = {'chapter': 250, 'title': 250, 'subtitle': 250, 'body': 10000 }

$(document).ready(function(){
        var formName = $('#formName').val();
        if (formName == 'story'){
            id_fields = id_fields_story;
            $('#chapter').keyup(function () {

            var id_label = '#story_chapter';
            var max = id_fields['title'];

            var len = $(this).val().length;
            var ch = max - len;
            if (len > max) {
                $(id_label).text('You need delete ' + ch);
                $(id_label).removeClass('black');
                 $(id_label).addClass('red');
            }
            else {
                $(id_label).text(ch + ' characters left');
                $(id_label).addClass('black');
                $(id_label).removeClass('red');
            }
        });

            $('#title').keyup(function () {

            var id_label = '#story_title';
            var max = id_fields['title'];

            var len = $(this).val().length;
            var ch = max - len;
            if (len > max) {
                $(id_label).text('You need delete ' + ch);
                $(id_label).removeClass('black');
                 $(id_label).addClass('red');
            }
            else {
                $(id_label).text(ch + ' characters left');
                $(id_label).addClass('black');
                $(id_label).removeClass('red');
            }
        });

            $('#subtitle').keyup(function () {
            var id_label = '#story_subtitle'
            var max = id_fields['subtitle'];

            var len = $(this).val().length;
            var ch = max - len;
            if (len > max) {
                $(id_label).text('You need delete ' + ch);
                $(id_label).removeClass('black');
                 $(id_label).addClass('red');
            }
            else {
                $(id_label).text(ch + ' characters left');
                $(id_label).addClass('black');
                $(id_label).removeClass('red');
            }
        });

            $('#body').keyup(function () {
        var id_label = '#story_body'
        var max = id_fields['body'];

        var len = $(this).val().length;
        var ch = max - len;
        if (len > max) {
            $(id_label).text('You need delete ' + ch);
            $(id_label).removeClass('black');
             $(id_label).addClass('red');
        }
        else {
            $(id_label).text(ch + ' characters left');
            $(id_label).addClass('black');
            $(id_label).removeClass('red');
        }
    });
        }
        else {
            id_fields = id_fields_news;
            if (formName.slice(formName.indexOf('_')) == '_novel') {
                id_fields = id_fields_novel;
            }
            $('#title').keyup(function () {

            var id_label = '#' + formName + '_' + 'title';
            var max = id_fields['title'];

            var len = $(this).val().length;
            var ch = max - len;
            if (len > max) {
                $(id_label).text('You need delete ' + ch);
                $(id_label).removeClass('black');
                 $(id_label).addClass('red');
            }
            else {
                $(id_label).text(ch + ' characters left');
                $(id_label).addClass('black');
                $(id_label).removeClass('red');
            }
        });

            $('#subtitle').keyup(function () {
            var id_label = '#' + formName + '_' + 'subtitle'
            var max = id_fields['subtitle'];

            var len = $(this).val().length;
            var ch = max - len;
            if (len > max) {
                $(id_label).text('You need delete ' + ch);
                $(id_label).removeClass('black');
                 $(id_label).addClass('red');
            }
            else {
                $(id_label).text(ch + ' characters left');
                $(id_label).addClass('black');
                $(id_label).removeClass('red');
            }
        });

            $('#body').keyup(function () {
        var id_label = '#' + formName + '_' + 'body'
        var max = id_fields['body'];

        var len = $(this).val().length;
        var ch = max - len;
        if (len > max) {
            $(id_label).text('You need delete ' + ch);
            $(id_label).removeClass('black');
             $(id_label).addClass('red');
        }
        else {
            $(id_label).text(ch + ' characters left');
            $(id_label).addClass('black');
            $(id_label).removeClass('red');
        }
    });
    }
});


