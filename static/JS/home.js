
$(document).ready(function () {
 /*
    $('input').click(function () {
        $('#box').load('test.html');
        alert('click now');
    });
*/

    $('input').click(function () {
        $.get('/douban/export/', {
            'rows_num': 100
        }, function (response, status, xhr) {
            if (status == 'success') {
                $('body').html(response);
            }
        })
    });
});