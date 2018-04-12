// Add on click handlers for buttons.
$(document).ready(function() {
  $('#linkedin').attr('href', 'https://www.linkedin.com/in/johnrarendt/');
  $('#linkedin').attr('target', '_blank');

  $('#email').attr('href', 'mailto://jack.arendt93@gmail.com');
  $('#email').attr('target', '_blank');

  $('#github').attr('href', 'https://www.github.com/jackarendt/website');
  $('#github').attr('target', '_blank');

  $('#instagram').attr('href', 'https://www.instagram.com/jack.arendt/');
  $('#instagram').attr('target', '_blank');

  $('#contact-form').submit(function() {
    return false;
  });
});
