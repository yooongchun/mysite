/*----------------评论功能-----------------*/
$(document).ready(function () {
    /*---------------------评论消息--------------------*/
    //选择头像
    $(".comment-box .comment").each(function () {
        let parent = $(this);
        parent.find(".show-ico-btn").click(function () {
            parent.find('.pop-ico').fadeIn();
            parent.find(".ico-list").find("a").each(function () {
                $(this).bind("click", function () {
                    parent.find(".show-ico-btn").find("img").attr("src", $(this).find("img").attr("src"));
                    parent.find(".pop-ico").fadeOut();
                });
            });
        });
        //回送消息
        parent.find(".comment-submit").click(function () {
            send_comment_data(parent, 0);
        });
    });
    /*---------------------回复评论--------------------*/
    $(".comment-display-list .comment-reply-btn").each(function () {
        let parent = $(this).parent().parent().parent().parent();
        //显示评论框
        $(this).click(function () {
            parent.find(".reply-comment").fadeIn();
        });
        //选择头像
        parent.find(".show-ico-btn").click(function () {
            parent.find(".pop-ico").fadeIn();
        });
        parent.find(".ico-list").find("a").each(function () {
            $(this).bind("click", function () {
                parent.find(".show-ico-btn").find("img").attr("src", $(this).find("img").attr("src"));
                parent.find(".pop-ico").fadeOut();
            });
        });
        //回送数据
        parent.find(".comment-submit").click(function () {
            let parent_comment_id = Number(parent.attr("data-value"));
            send_comment_data(parent, parent_comment_id);
        });
    });
});

/*-----------------------依赖函数---------------------*/

//发送评论数据
function send_comment_data(parent, parent_comment_id) {
    let user = parent.find(".nick-name").val();
    let email = parent.find(".email").val();
    let content = parent.find(".comment-content").val();
    let reply = parent.find(".comment-reply").is(':checked');
    let COMMENT_SUCCESS_RETURN_INFO = '评论成功';
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
        // alert("评论内容不能为空~");
        parent.find(".response-comment-info").text("评论内容不能为空~");
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
            'need-reply': reply,
            'comment-time': (new Date()).valueOf(),
            'parent-comment-id': parent_comment_id,
            'type': 'COMMENT',
        },
        function (data) {
            //显示回传信息
            parent.find(".response-comment-info").text(data);
            parent.find(".response-comment-info-box").fadeIn();
            setTimeout(function () {
                parent.find(".response-comment-info-box").fadeOut();
            }, 1000);
            //成功的评论则重载页面
            if (data === COMMENT_SUCCESS_RETURN_INFO) {
                setTimeout(function () {
                    window.location.href = window.location.href + "#comment-display-list";
                    window.location.reload();

                }, 1000);
            }
        });
}


function setCookie(cname, cvalue, exdays) {
    /*设置cookie*/
    let d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    /*获取cookie*/
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        let c = ca[i].trim();
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie(cookieName) {
    /*检查cookie是否存在*/
    return getCookie(cookieName) !== "";
}