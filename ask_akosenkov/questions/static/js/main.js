// var myImage = document.querySelector('img');
//
// myImage.onclick = function() {
//     myImage.setAttribute ('src','/media/default/Chloe.jpg');
// };
//
// // $.get - вызов метода get (GET запрос) объекта jQuery (инкапсулирован в переменной $)
// // 1-й параметр - урл, куда идет запрос, 2-й - какие данные передаются,
// // 3-й - callback-функция - функция, которая сработает после отправки запроса и получения ответа на него
// // 4-й параметр - какой тип данных ожидается в ответ
// $.get('/like', {key: 'value'}, function(data) {
//     // Запись данных в блок с id = some_block
//     $("#some_block").html(data)
// //    console.log(data)
// }, "json");

// $("button").on('.fa-thumbs*', {}, function(){});
// Можно использовать itemid - атрибут подпункта меню, который будет засовывать в url указанн

$(".like_dislike_ajax").on('click', 'button', function(event) {
    // console.log('ajax for like dislike here!');
    // console.log($(this));
    var form = $(this).parent().parent();
    var rating = form.parent().parent().find('.vote_rating');
    var icon = $(this).children('i');
    // console.log(icon);
    // icon.removeClass('like_active');
    // icon.removeClass('fas');
    // icon.addClass('far');

    var csrf = form.children("input[name='csrfmiddlewaretoken']").val();
    var vote_object = form.children("input[name='type']").val();
    var vote_type = $(this).hasClass('like_button') ? 'Like' : 'Dislike';
    var vote_id = form.children("input[name='id']").val();

    var data = {
        vote: vote_type,
        type: vote_object,
        id: vote_id,
        csrfmiddlewaretoken: csrf,
    };

    // console.log(data);
    if (!(icon.hasClass('vote_active'))) {
        var search_type = vote_type === 'Like' ? 'dislike_button' : 'like_button';
        var neighbour_button = form.find(`button.${search_type}`);
        var neighbour_icon = neighbour_button.children('i');
        console.log(neighbour_button);
        if (neighbour_icon.hasClass('vote_active')) {
            neighbour_icon.removeClass('fas vote_active');
            neighbour_icon.addClass('far');
        }
        $.ajax({
            url: "", // the endpoint
            type: "POST", // http method
            data: data, // data sent with the post request
            dataType: 'json',

            // handle a successful response
            success: function (data) {
                console.log(data); // log the returned json to the console
                console.log("success"); // another sanity check
                if (data.status === 'success') {
                    icon.removeClass('far');
                    icon.addClass('fas vote_active');
                    rating.html(data.rating);
                } else {
                    $('.ajax_error').html(
                        "<div class=\"alert alert-danger mt-3\" role=\"alert\">Internal error " + data.message + "</div>"
                    )
                }
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('.ajax_error').html(
                    "<div class=\"alert alert-danger mt-3\" role=\"alert\">Internal error: " + errmsg + "</div>"
                ); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
});