//处理友情链接申请
$(document).ready(function () {
    $('.apply-link-box .submit-apply-link-info').click(function () {
        let parent = $('.apply-link-box');
        let site_name = parent.find('input.link-site-name').val();
        let url = parent.find('input.link-url').val();
        let description = parent.find('input.link-description').val();
        let target_url = 'http://' + window.location.host.toString() + '/blog/friendlink/';
        $.post(target_url, {
            'type': 'FRIENDLINK',
            'site_name': site_name,
            'url': url,
            'description': description
        }, function (data) {
            alert(data);
        });
    });
});