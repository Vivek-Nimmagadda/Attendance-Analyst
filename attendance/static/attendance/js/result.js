$(function () {
   $("#table-75").hide();
});

var time = 0;

$("#75-btn").bind('click', function (event) {
    $(this).addClass('active');
    $('#80-btn').removeClass('active');
    $('#table-80').hide(time);
    $('#table-75').show(time);
});

$("#80-btn").bind('click', function (event) {
    $(this).addClass('active');
    $('#75-btn').removeClass('active');
    $('#table-75').hide(time);
    $('#table-80').show(time);
});