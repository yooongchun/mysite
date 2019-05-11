//导航栏滚动消息
$(document).ready(function () {
    var $uList = $("#info-list");
    var timer = null;
    $uList.hover(function () {
            clearInterval(timer);
        },
        function () {
            timer = setInterval(function () {
                scrollList($uList);
            }, 2000);
        }).trigger("mouseleave");

    function scrollList() {
        var scrollHeight = $("ul li:first").height();
        $uList.stop().animate({
                marginTop: -scrollHeight
            }, 600,
            function () {
                $uList.css({
                    marginTop: 0
                }).find("li:first").appendTo($uList);
            });
    }
});
