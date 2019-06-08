/*公用功能*/
$(document).ready(function () {
    //弹出框
    $('#wechat-official-account').popover({
        trigger: 'hover',
        html: true,
    });
    $('#wechat-add-friend').popover({
        trigger: 'hover',
        html: true,
    });
    //密码输入框
    $('.article-input-password').each(function () {
        $(this).popover({
            html: true,
        });
    });

    //注册用户选择头像
    choose_register_user_icon();

    //适配手机
    fit_mobile();

    //设置摄影图片属性
    set_photograph_img_attr();
    //申请链接
    $('#apply-link-btn').popover({
        html: true,
    });
    //更新时间
    update_time();
    //提示框
    $('[data-toggle="tooltip"]').tooltip();
    //当跳转到分类页面时触发导航栏的分类标签状态改变函数
    change_current_category();
    //editor.md渲染
    editormd.markdownToHTML("editormd-box", {
        id: "editormd",
        path: "../lib/",
        htmlDecode: "style,script,iframe", // you can filter tags decode
        emoji: true,
        tocm: true,
        toc: true,
        taskList: true,
        tex: true, // 默认不解析
        table: true,
        flowChart: true, // 默认不解析
        sequenceDiagram: true, // 默认不解析
    });

    //监听屏幕滚动
    window.onscroll = function () {
        let t = document.documentElement.scrollTop || document.body.scrollTop; //获取距离页面顶部的距离
        let uptop = $(".go-to-top"); //获取div元素
        if (t >= 300) { //当距离顶部超过300px时
            uptop.css({
                'top': window.innerHeight + t - 200 + 'px',
                'display': 'inline'
            });
        }
    };
    //回到顶部按钮
    let timer = null;
    $(".go-to-top .go-top-img").click(function () { //点击图片时触发点击事件
        timer = setInterval(function () { //设置一个计时器
            let t = document.documentElement.scrollTop || document.body.scrollTop; //获取距离页面顶部的距离
            t -= 300;
            if (t > 0) { //如果与顶部的距离大于零
                window.scrollTo(0, t);
            } else { //如果距离小于等于零
                window.scrollTo(0, 0); //移动到顶部
                clearInterval(timer); //清除计时器
            }
        }, 10);
    });
});

function change_current_category() {
    /*分类跳转时导航栏标签状态改变*/
    let category = $('title').attr('data-value');
    $(".nav-category").each(function () {
        let parent = $(this);
        if (category === parent.text()) {
            $('.nav-category').removeClass('active');
            parent.addClass("active");
        }
    });
}

function update_time() {
    /*更新时间*/
    let start_timestamp = 1551259142443;
    setInterval(function () {
        let timestamp = Date.parse(new Date()) - start_timestamp;
        let yms = 1000 * 3600 * 24 * 30 * 12;
        let mms = 1000 * 3600 * 24 * 30;
        let dms = 1000 * 3600 * 24;
        let hms = 1000 * 3600;
        let year = parseInt(timestamp / yms);
        let month = parseInt((timestamp - year * yms) / mms);
        let day = parseInt((timestamp - year * yms - month * mms) / dms);
        let hours = parseInt((timestamp - year * yms - month * mms - day * dms) / hms);
        let minutes = parseInt((timestamp - year * yms - month * mms - day * dms - hours * hms) / 60 / 1000);
        let seconds = parseInt((timestamp - year * yms - month * mms - day * dms - hours * hms - minutes * 60 * 1000) / 1000);
        $(".years").text(year);
        $(".months").text(month);
        $(".days").text(day);
        $(".hours").text(hours);
        $(".minutes").text(minutes);
        $(".seconds").text(seconds);
    }, 1000);

}

function set_photograph_img_attr() {
    /*设置摄影图片属性*/
    $('.photograph-box span').each(function () {
        let nums = parseInt($(this).attr('data-value').split('-')[0]);
        let num = parseInt($(this).attr('data-value').split('-')[1]);
        let rotY = parseInt(360 / nums * num).toString();
        $(this).css('transform', 'rotateY(' + rotY + 'deg) translateZ(650px)');
        $('.bg').css('background-image', 'url("../../static/blog/images/love.jpg")');
        $(this).mouseover(function () {
            $('.photograph-box').css('animation-play-state', 'paused');
            $(this).find('img').animate({
                width: '336',
                height: '480',
                opacity: '1'
            }, 'slow');
        }).mouseout(function () {
            $('.photograph-box').css('animation-play-state', 'running');
            $(this).find('img').animate({
                width: '280',
                height: '400',
                opacity: '0.8'
            }, 'slow');
        });
    });
}

function fit_mobile() {
    /*适配手机*/
    if (isMobile()) {
        $('#base-right-side').remove();
        $('#left-container').removeClass('col-sm-9').addClass('container-fluid');
        $('.container').css('width', '100%');
        $('.main-box').css('margin-top', '150px');
    }
}

function isMobile() {
    /*判断访问设备是否为手机*/
    var userAgentInfo = navigator.userAgent;

    var mobileAgents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];

    var mobile_flag = false;

    //根据userAgent判断是否是手机
    for (var v = 0; v < mobileAgents.length; v++) {
        if (userAgentInfo.indexOf(mobileAgents[v]) > 0) {
            mobile_flag = true;
            break;
        }
    }

    var screen_width = window.screen.width;
    console.log(screen_width);

    //根据屏幕分辨率判断是否是手机
    if (screen_width < 576) {
        mobile_flag = true;
    }
    console.log(mobile_flag);
    return mobile_flag;
}



//写cookies 
function setCookie(name, value) {
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

//读取cookies 
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

//删除cookies 
function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

//登陆校验
function login_check() {
    let user_name = $("#user-name").val();
    let password = $("#password").val();
    if (user_name === "" || password === "") {
        $("#response-login-info").text("账号或者密码不能为空！");
        let info_box = $(".response-login-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    }
    url = window.location.protocol + "//" + window.location.host + "/login/";
    $.post(url, {
        user_name: user_name,
        password: password
    }, function (data, status) {
        if (data === "user-not-exists") {
            $("#response-login-info").text("用户不存在！");
            let info_box = $(".response-login-info-box");
            info_box.fadeIn();
            setTimeout(function () {
                info_box.fadeOut();
            }, 1000);
        } else if (data === "404") {
            $("#response-login-info").text("密码错误！");
            let info_box = $(".response-login-info-box");
            info_box.fadeIn();
            setTimeout(function () {
                info_box.fadeOut();
            }, 1000);
        } else if (data.split("|")[0] === "200") {
            $("#response-login-info").text("登陆成功，一秒后自动关闭！");
            setCookie("path", window.location.protocol + "//" + window.location.host);
            setCookie("username", user_name);
            setCookie("password", password);

            $("#login-info-box").html(`<image src="${data.split('|')[1]}" alt='user-icon' width=20 height=20 class='rounded-circle' /><a href='javascript:void(0);'>${user_name}</a>`);
            let info_box = $(".response-login-info-box");
            info_box.fadeIn();
            setTimeout(function () {
                info_box.fadeOut();
                $("#login-modal-close-btn").click();
            }, 2000);

        } else {
            $("#response-login-info").text("未知错误！");
            let info_box = $(".response-login-info-box");
            info_box.fadeIn();
            setTimeout(function () {
                info_box.fadeOut();
            }, 1000);

        }

    });
}


//注册选择头像
function choose_register_user_icon() {
    //选择头像
    $(".register-icon-box .show-ico-btn").click(function () {
        $('.register-icon-box .pop-ico').fadeIn();
        $(".register-icon-box .ico-list").find("a").each(function () {
            $(this).bind("click", function () {
                $(".register-icon-box .show-ico-btn").find("img").attr("src", $(this).find("img").attr("src"));
                $(".register-icon-box .pop-ico").fadeOut();
            });
        });
    });
}


//注册
function register() {
    let user_name = $("#register-user-name").val();
    let password = $("#register-password").val();
    let password_verify = $("#register-password-verify").val();
    let email = $("#register-email").val();
    let icon = $(".register-icon-box .comment-img").attr("src");

    if (user_name === "") {
        $("#response-register-info").text("用户名不能为空！");
        let info_box = $(".response-register-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    } else if (password === "") {
        $("#response-register-info").text("密码不能为空！");
        let info_box = $(".response-register-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    } else if (email === "") {
        $("#response-register-info").text("邮箱不能为空！");
        let info_box = $(".response-register-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    } else if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
        $("#response-register-info").text("邮箱地址不合法！");
        let info_box = $(".response-register-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    } else if (password !== password_verify) {
        $("#response-register-info").text("密码不一致！");
        let info_box = $(".response-register-info-box");
        info_box.fadeIn();
        setTimeout(function () {
            info_box.fadeOut();
        }, 1000);
        return;
    } else {
        url = window.location.protocol + "//" + window.location.host + "/register/";
        $.post(url, {
            username: user_name,
            password: password,
            email: email,
            icon: icon,
        }, function (data, status) {
            if (data === "user-exists") {
                $("#response-register-info").text("用户已存在！");
                let info_box = $(".response-register-info-box");
                info_box.fadeIn();
                setTimeout(function () {
                    info_box.fadeOut();
                }, 1000);

            } else if (data === "200") {
                $("#response-register-info").text("注册成功，一秒后自动关闭！");
                setCookie("path", window.location.protocol + "//" + window.location.host);
                setCookie("username", user_name);
                setCookie("password", password);

                $("#login-info-box").html(`<image src="${icon}" alt='user-icon' width=20 height=20 class='rounded-circle' /><a href='javascript:void(0);'>${user_name}</a>`);
                let info_box = $(".response-register-info-box");
                info_box.fadeIn();
                setTimeout(function () {
                    info_box.fadeOut();
                    $("#register-modal-close-btn").click();
                }, 2000);
            } else if (data === "create-user-error") {
                $("#response-register-info").text("创建用户出错！");
                let info_box = $(".response-register-info-box");
                info_box.fadeIn();
                setTimeout(function () {
                    info_box.fadeOut();
                }, 1000);
            } else {
                $("#response-register-info").text("未知错误！");
                let info_box = $(".response-register-info-box");
                info_box.fadeIn();
                setTimeout(function () {
                    info_box.fadeOut();
                }, 1000);
            }
        });

    }

}