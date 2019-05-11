// Expose jQuery to the global object
window.jQuery = window.$ = jQuery;

// main object
var BwShortcode = {

	init: function () {

		//this.bargraph();
		this.toggle();

	},

	// bar graph
	bargraph: function () {
		if ($('.bargraph').length > 0) {
			$('.bargraph li').each(function () {
				$('.bar-wrap span', this).addClass('visible');
				TweenLite.to($('.bar-wrap span', this), 1.8, { delay: 0.15, width: $('.bar-wrap span', this).attr('data-width') + '%', ease: Expo.easeInOut });
			});
		}
	},

	// faq toggle
	toggle: function () {
		$(document).on('click', '.toggle-title', function () {

			var $toggle = $(this).closest('.toggle');
			var $toggleContent = $toggle.find('.toggle-content');

			if (!$toggle.hasClass('active')) {
				$toggleContent.stop(true, true).slideDown(300);
			} else {
				$toggleContent.stop(true, true).slideUp(300);
			}

			$toggle.toggleClass('active');
		});
	}

};

BwShortcode.init();