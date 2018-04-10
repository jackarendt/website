// Add on click handlers for buttons.
$(document).ready(function() {
  var socialClickHandler = function() {
    const links = {
      'linkedin' : 'https://www.linkedin.com/in/johnrarendt/',
      'email' : 'mailto://jack.arendt93@gmail.com',
      'github' : 'https://www.github.com/jackarendt',
      'instagram' : 'https://www.instagram.com/jack.arendt/'
    };

    const link = links[this.id];
    if (link != null) {
      window.open(link, '_blank');
    }
  };

  $('#linkedin').click(socialClickHandler);
  $('#email').click(socialClickHandler);
  $('#github').click(socialClickHandler);
  $('#instagram').click(socialClickHandler);
});
