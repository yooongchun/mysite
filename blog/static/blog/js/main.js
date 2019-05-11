window.$ = window.$ = $;

let $body = $('body');
let $window = $(window);
let self;

let App = {
    firstPage: true,
    start: function () {
        "use strict";
        self = this;
        if ($('body').hasClass('image-copyright')) {
            App.image_copyright();
        }
        App.pageAnimations('in');
    },
    image_copyright: function () {
        "use strict";
        let copyTimer;

        $(document).on('contextmenu', '.copyright, #kenburns img, #fotorama img, .bw-owl-slider img, .mfp-img', function (e) {
            clearTimeout(copyTimer);
            $('#image-copyright').show().css('top', e.screenY / 2).css('left', e.screenX / 2);
            copyTimer = setTimeout(function () {
                $('#image-copyright').fadeOut(150);
            }, 2000);
            return false;
        });

    },
    addthis: function () {
        "use strict";
        if ($('#bw-share').length || $('#bw-share-gallery').length) {
            if (typeof (window.addthis) !== 'undefined') {
                window.addthis = null;
                window._adr = null;
                window._atc = null;
                window._atd = null;
                window._ate = null;
                window._atr = null;
                window._atw = null;
            }
            $.getScript('//s7.addthis.com/js/300/addthis_widget.js#pubid=ra-534b93e766f14c42');
        }
    },
    cf7: function () {
        "use strict";
        if ($('#bw-cf7').length && !App.firstPage) {

            _wpcf7.supportHtml5 = $.wpcf7SupportHtml5();
            $('div.wpcf7 > form').wpcf7InitForm();

        }
    },
    bind: function () {
        "use strict";
        // add this rail gallery effect
        $(document).on('click', '#rail-buttons .rail-addthis', function () {

            let self = $(this);
            let element = $('#bw-share-gallery a');
            let c = 0;

            if (self.hasClass('animate')) {
                return;
            }

            if (!self.hasClass('open')) {

                self.addClass('open');

                TweenMax.staggerTo(element, 0.3,
                    {opacity: 1, visibility: 'visible'},
                    0.075);
                TweenMax.staggerTo(element, 0.3,
                    {top: -12, ease: Cubic.easeOut},
                    0.075);

                TweenMax.staggerTo(element, 0.2,
                    {
                        top: 0, delay: 0.1, ease: Cubic.easeOut, onComplete: function () {
                            c++;
                            if (c >= element.length) {
                                self.removeClass('animate');
                            }
                        }
                    },
                    0.075);

                self.addClass('animate');

            } else {

                TweenMax.staggerTo(element, 0.3,
                    {
                        opacity: 0, onComplete: function () {
                            c++;
                            if (c >= element.length) {
                                self.removeClass('open animate');
                                element.css('visibility', 'hidden');
                            }
                            ;
                        }
                    },
                    0.075);

            }

        });

    },

    pageAnimations: function (direction) {
        "use strict";
        let e = $('#djax > #content > div, #djax > #content > article');

        switch (direction) {
            case 'in': {
                App.play.slider.start('in');
                App.addthis();
                App.cf7();

                if (e.hasClass('bw--mp')) {
                    App.play.mp.start('in');
                }
                if (e.hasClass('bw--article')) {
                    App.play.article();
                }
                if (e.hasClass('bw--page')) {
                    App.play.graph();
                }
                if (e.hasClass('bw--white')) {
                    App.play.white.start(e);
                }

                if (e.hasClass('bw--rail')) {
                    App.play.rail.start('in');
                    break;
                }
                if (e.hasClass('bw--isotope')) {
                    App.play.isotope.start('in');
                    break;
                }
                if (e.hasClass('bw--fotorama')) {
                    App.play.fotorama.start('in');
                    break;
                }
                if (e.hasClass('bw--kenburns')) {
                    App.play.kenburns.start('in');
                    break;
                }

                break;

            }
            case 'out': {

                App.play.slider.start('out');

                if (e.hasClass('bw--mp')) {
                    App.play.mp.start('out');
                }
                if (e.hasClass('bw--rail')) {
                    App.play.rail.start('out');
                    break;
                }
                if (e.hasClass('bw--isotope')) {
                    App.play.isotope.start('out');
                    break;
                }
                if (e.hasClass('bw--fotorama')) {
                    App.play.fotorama.start('out');
                    break;
                }
                if (e.hasClass('bw--kenburns')) {
                    App.play.kenburns.start('out');
                    break;
                }

                break;
            }

            default:
                break;
        }

    },
    play: {
        slider: {
            start: function (direction) {
                "use strict";
                self = this;
                switch (direction) {
                    case 'in': {
                        self.run();
                        self.bind();
                        break;
                    }
                    case 'out': {
                        self.stop();
                        break;
                    }

                    default:
                        break;
                }
            },
            run: function () {
                "use strict";
                // box slider
                if ($('#boxgallery').length > 0) {

                    new BoxesFx(document.getElementById('boxgallery'));

                }

                // owl carousel
                let $owlSlider = $('.bw-owl-slider');

                if ($owlSlider.length > 0) {

                    $owlSlider.each(function () {
                        let self = $(this);
                        self.owlCarousel({
                            items: 1,
                            singleItem: true,
                            lazyLoad: true,
                            pagination: true,
                            navigationText: false,
                            transitionStyle: (self.attr('data-effect')) ? (self.attr('data-effect')) : false
                        });
                    });


                }

            },
            bind: function () {
                "use strict";
                let portfolioToggle = $('.portfolio-toggle'),
                    portfolio = $('.bw-portfolio');

                if (portfolioToggle.length) {
                    portfolioToggle.bind('click', function () {
                        portfolio.toggleClass('expand');
                    });
                }

            },
            stop: function () {
            }
        },
        rail: {

            start: function (direction) {
                "use strict";
                self.railIndex = 1;

                switch (direction) {

                    case 'in': {

                        App.play.rail.length();
                        App.play.rail.focus(self.railIndex);
                        App.play.rail.mousewheel();
                        App.play.rail.cursors();
                        App.play.rail.nav();
                        App.play.rail.bind();

                        break;
                    }
                    case 'out': {

                        $('#rail-screen').unbind();

                        break;
                    }
                    default:
                        break;
                }

            },

            bind: function () {
                "use strict";
                if ($body.hasClass('bw-is-mobile')) {

                    $('.bw--rail').bind("swipeleft", function () {
                        App.play.rail.focus(self.railIndex + 1);
                    });

                    $('.bw--rail').bind("swiperight", function () {
                        App.play.rail.focus(self.railIndex - 1);
                    });

                }

            },

            nav: function () {
                "use strict";
                $(document).on('click', '#rail.rail-next, #rail-buttons .rail-next', function () {
                    if (!$('#rail').hasClass('animate')) {
                        App.play.rail.focus(self.railIndex + 1);
                    }
                });

                $(document).on('click', '#rail.rail-prev, #rail-buttons .rail-prev', function () {
                    if (!$('#rail').hasClass('animate')) {
                        App.play.rail.focus(self.railIndex - 1);
                    }
                });

            },

            mousewheel: function () {
                "use strict";
                $(window)
                    .unbind('mousewheel')
                    .mousewheel(function (e, d) {

                        if (!$('#rail').hasClass('animate') && !$('#main-menu').hasClass('visible')) {
                            if (d > 0) {
                                // scroll up
                                App.play.rail.focus(self.railIndex - 1);
                            } else {
                                // scroll down
                                App.play.rail.focus(self.railIndex + 1);
                            }
                        }
                    });
            },

            cursors: function () {
                "use strict";
                $('#rail img').on('mouseenter', function () {

                    let $this = $(this);

                    $('#rail').removeClass('rail-next rail-prev');

                    switch (true) {

                        case ($this.index() > self.railIndex): {

                            $('#rail').addClass('rail-next');

                            break;
                        }
                        case ($this.index() < self.railIndex): {

                            $('#rail').addClass('rail-prev');

                            break;
                        }
                        default:
                            return;
                    }

                });

            },

            focus: function (index) {
                "use strict";
                if ($('#rail img:eq(' + index + ')').length && !$('#rail').hasClass('animate') && index >= 0) {

                    $('#rail-buttons a span').removeClass('unactive');

                    if (index === 0) {
                        $('.rail-prev span').addClass('unactive');
                    }

                    if (index + 1 >= $('#rail img').length) {
                        $('.rail-next span').addClass('unactive');
                    }

                    self.railIndex = index;

                    $('#rail').addClass('animate');

                    let elementLeftPosition = parseInt($('#rail img:eq(' + index + ')').position().left, 10);

                    let centerPosition = (elementLeftPosition - ($window.width() * 0.5)) + $('#rail img:eq(' + index + ')').width() * 0.5;

                    TweenMax.to($('#rail img:not(:eq(' + index + '))'), 0.3, {delay: 0.3, opacity: 0.3});
                    TweenMax.to($('#rail img:eq(' + index + ')'), 0.3, {delay: 0.3, opacity: 1});

                    $('#rail img').removeClass('focus');
                    $('#rail img:eq(' + index + ')').addClass('focus');

                    TweenMax.to($('#rail-slider'), 0.8, {
                        left: -centerPosition, ease: Expo.easeInOut, onComplete: function () {

                            $('#rail').removeClass('animate');

                        }
                    });

                    App.play.rail.info(index);

                }

            },

            info: function (index) {
                "use strict";
                let $hidden = $('.rail-hidden'),
                    $info = $('#rail-info'),
                    title = $('li:eq(' + index + ')', $hidden).attr('data-title');

                TweenMax.to($('.img-title', $info), 0.3, {
                    opacity: 0, bottom: -60, ease: Cubic.easeIn, onComplete: function () {
                        $('.img-title', $info).html(title);
                        TweenMax.to($('.img-title', $info), 0.3, {opacity: 1, bottom: 0, ease: Cubic.easeOut});
                    }
                });

                TweenMax.to($('.img-desc', $info), 0.3, {
                    opacity: 0, top: -40, ease: Cubic.easeIn, onComplete: function () {
                        let source = '';
                        source += $('#rail-source li:eq(' + index + ')').html();
                        $('.img-desc', $info).html((index + 1) + ' ' + $info.attr('data-from') + ' ' + $('li', $hidden).length + ' ' + $info.attr('data-photos') + ((($.trim(source) !== '') ? '<br/>' : '') + source));
                        TweenMax.to($('.img-desc', $info), 0.3, {opacity: 1, top: 0, ease: Cubic.easeOut});
                    }
                });

            },

            length: function () {
                "use strict";
                let totalRailWidth = 0;

                $('#rail img').each(function () {
                    totalRailWidth += parseInt($(this).width(), 10);
                });

                totalRailWidth += 3000;

                $('#rail-slider').width(totalRailWidth);
                $('#rail').width(totalRailWidth + (totalRailWidth * 0.01));
            }
        }
    },
};

$(window).load(function () {
    "use strict";
    load_img();
    App.start();
});

//ajax动态请求图片
function load_img() {
    $("#rail img").each(function () {
        let img_obj = $(this);
        let src = $(this).attr("src");
        if (src.indexOf("loading") > -1 && src.indexOf(".gif") > -1) {
            $.post("", {"id": $(this).attr("data-value")}, function (data) {
                let id = img_obj.attr("data-value");
                let url = data.split("|")[0];
                let story = data.split("|")[1];
                console.log(url);
                console.log(story);
                console.log(id);
                img_obj.attr("src", url);
                $("#" + id).text(story);
            });
        }
    });
}
