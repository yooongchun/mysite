/*点赞功能*/
$(document).ready(function () {
    let flag = 'APPROVAL';
    //ajax传递消息
    $(".approval-item").each(function () {
        let parent = $(this);
        let article_id = $(this).attr('data-value');
        $(this).click(function () {
            let url = 'http://' + window.location.host.toString() + '/approval/';
            $.post(url, {'type': flag, 'article-id': article_id}, function (data) {
                approvalAnimation(parent, data, 2000);
            });

        });
    });
});

function approvalAnimation(parent, data, timeGap) {
    //点赞特效
    parent.append("<img alt='approval' src='' style='position: absolute;width: 20px;height: 20px;margin-left: -20px;'>");
    let num = Math.floor(Math.random() * 4 + 1);
    let rand = parseInt(Math.random() * 500 * (Math.round(Math.random() * 2) - 1));
    parent.find("img").attr('src', '/static/blog/images/ap' + num + '.png');
    if (data.indexOf('已经点过赞') === -1) {
        let curValue = Number(parent.find(".approval-num").text());
        parent.find(".approval-num").text((curValue + 1).toString());

    }
    parent.find("img").animate({
        bottom: "600px",
        opacity: "0",
        marginLeft: rand.toString() + 'px',
        width: '50px',
        height: '50px',
    }, timeGap);
}