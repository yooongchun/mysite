/*----------------留言功能-----------------*/
$(document).ready(function () {
    if ($("title").text() === '留言') {
        //选择头像
        $(".message-container .show-ico-btn").click(function () {
            $(".message-container .pop-ico").fadeIn();
        });
        $("> a", ".message-container .ico-list").each(function () {
            $(this).bind("click", function () {
                $(".message-container .show-ico-btn").find("img").attr("src", $(this).find("img").attr("src"));
                $(".message-container .pop-ico").fadeOut();
            });
        });
        //回送消息
        $(".message-container .comment-submit").click(function () {
            send_message_data($(".message-container"));
        });
    }
});

//发送留言数据
function send_message_data(parent) {
    let user = parent.find(".nick-name").val();
    let email = parent.find(".email").val();
    let content = parent.find(".comment-content").val();
    let reply = parent.find(".comment-reply").is(':checked');
    let title = parent.find(".message-title-text").val();
    let MESSAGE_SUCCESS_RETURN_INFO = '留言成功';
    if (user === "") {
        //提示信息
        // alert("用户名不能为空~");
        parent.find(".response-comment-info").text("用户名不能为空~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    }
    if (email === "") {
        //提示信息
        // alert("邮箱地址不能为空~");
        parent.find(".response-comment-info").text("邮箱地址不能为空~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    }
    if (email.indexOf('@') === -1) {
        //提示信息
        // alert("邮箱地址不正确~");
        parent.find(".response-comment-info").text("邮箱地址不正确~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    }
    if (content === "") {
        //提示信息
        // alert("留言内容不能为空~");
        parent.find(".response-comment-info").text("留言内容不能为空~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    }
    if (title === "") {
        //提示信息
        // alert("标题不能为空~");
        parent.find(".response-comment-info").text("标题不能为空~");
        parent.find(".response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".response-comment-info-box").fadeOut();
        }, 1000);
        return;
    }
    $.post("",
        {
            'img': parent.find(".comment-img").attr('src'),
            'user-name': user,
            'email': email,
            'content': content,
            'title': title,
            'need-reply': reply,
            'comment-time': (new Date()).valueOf(),
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