/*----------------评论功能-----------------*/
$(document).ready(function () {
    /*---------------------评论消息--------------------*/
    $(".comment-box .comment-submit").click(function () {
        send_comment_msg($(".comment-box"), 0);
    });
    /*---------------------回复评论--------------------*/
    $(".comment-display-list .comment-reply-btn").each(function () {
        let parent = $(this).parent().parent().parent().parent();
        //显示评论框
        $(this).click(function () {
            parent.find(".reply-comment").fadeIn();
        });
        //回送数据
        parent.find(".comment-submit").click(function () {
            let parent_comment_id = Number(parent.attr("data-value"));
            send_comment_msg(parent, parent_comment_id);
        });
    });
});

/*-----------------------依赖函数---------------------*/
function send_comment_msg(parent, parent_comment_id) {
    let username = getCookie("username");
    let password = getCookie("password");
    let text = parent.find(".comment-content").val();
    let comment_need_reply_status = parent.find(".comment-reply").is(":checked");
    let comment_is_anonymous = parent.find(".comment-is-anonymous-box").is(":checked");
    let article_id = $("#article-comment-box").attr("data");
    if ((username === null || password === null) && comment_is_anonymous === false) {
        parent.find(".comment .response-comment-info").text("你还没有登陆，请登录或者选择匿名评论~");
        parent.find(".comment .response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".comment .response-comment-info-box").fadeOut();
        }, 1000);
        return;
    } else if (text === "") {
        parent.find(".comment .response-comment-info").text("评论内容不能为空~");
        parent.find(".comment .response-comment-info-box").fadeIn();
        setTimeout(function () {
            parent.find(".comment .response-comment-info-box").fadeOut();
        }, 1000);
        return;
    } else {
        if (comment_is_anonymous || username === "") {
            username = "匿名";
        }
        url = window.location.protocol + "//" + window.location.host + "/comment/" + article_id + '/';
        $.post(url, {
                'user-name': username,
                'content': text,
                'need-reply': comment_need_reply_status,
                'parent-comment-id': parent_comment_id,
                'is-anonymous': comment_is_anonymous,
                'article-id': article_id,
                'type': 'COMMENT',
            },
            function (data) {
                //显示回传信息
                parent.find(".comment .response-comment-info").text(data);
                parent.find(".comment .response-comment-info-box").fadeIn();
                setTimeout(function () {
                    parent.find(".comment .response-comment-info-box").fadeOut();
                }, 1000);
                //成功的评论则重载页面
                if (data === "评论成功") {
                    setTimeout(function () {
                        window.location.href = window.location.href + "#comment-display-list";
                        window.location.reload();
                    }, 1000);
                }
            });
    }
}