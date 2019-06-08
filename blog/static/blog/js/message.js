/*----------------留言功能-----------------*/
$(document).ready(function () {
    if ($("title").text() === '留言') {
        //回送消息
        $(".message-container .comment-submit").click(function () {
            send_message_data($(".message-container"));
        });
    }
});

//发送留言数据
function send_message_data(parent) {
    let username = getCookie("username");
    let password = getCookie("password");
    let content = parent.find(".comment-content").val();
    let reply = parent.find(".comment-reply").is(':checked');
    let is_anonymous = parent.find(".comment-is-anonymous-box").is(':checked');
    let title = parent.find(".message-title-text").val();
    let MESSAGE_SUCCESS_RETURN_INFO = '留言成功';
    if ((username === null || password === null) && is_anonymous === false) {
        //提示信息
        parent.find(".response-comment-info").text("请登陆或者选择匿名评论~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    } else if (title === "" || content === "") {
        //提示信息
        parent.find(".response-comment-info").text("标题或内容不能为空~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    } else {
        if (username === "" || is_anonymous) {
            username = "匿名"
        }
        $.post("", {
                'user-name': username,
                'content': content,
                'title': title,
                'need-reply': reply,
                'is-anonymous': is_anonymous,
                'type': 'MESSAGE',
            },
            function (data, status) {
                //显示回传信息
                parent.find(".response-comment-info").text(data);
                parent.find(".response-comment-info-box").fadeIn();
                setTimeout(function () {
                    parent.find(".response-comment-info-box").fadeOut();
                }, 1000);
                //成功的留言则重载页面
                if (data === MESSAGE_SUCCESS_RETURN_INFO) {
                    setTimeout(function () {
                        window.location.reload();
                        window.location.href = window.location.href + "#comment-display-list";
                    }, 1000);
                }
            });
    }
}