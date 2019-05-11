//资源页判断密码是否正确
$(document).ready(function () {
        if ($("title").text() === '资源') {
            let DEFAULT_PSD = '0';
            $('.resource-container .resource ').each(function () {
                let parent = $(this);
                parent.find(".download-addr").click(function () {
                    let id = $(this).attr("data-value");
                    $.post("", {'type': 'RESOURCE', 'resource-id': id}, function (data, status) {
                        let d = eval('(' + data + ')');
                        let input_psd = parent.find(".resource-password").val();
                        if (d['password'] === input_psd || d['password'] === DEFAULT_PSD) {
                            window.location.href = d['link'];
                        } else {
                            parent.find(".response-response-info").text("密码错误~");
                            parent.find(".response-resource-info-box").fadeIn();
                            setTimeout(function () {
                                parent.find(".response-resource-info-box").fadeOut();
                            }, 1000);
                        }
                    });
                })
            });
        }
    }
);