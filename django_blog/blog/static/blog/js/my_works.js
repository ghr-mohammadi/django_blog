$(function () {
    var $posts = $("div#posts div.card.mb-3");
    var $coments = $("div#comments div.card.col-11.mb-3");

    $posts.last().removeClass("mb-3");
    $coments.last().removeClass("mb-3");
});
