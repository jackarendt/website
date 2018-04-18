// Add on click handlers for buttons.
$(document).ready(function() {

  var encodeQueryData = function(data) {
    let ret = [];
    for (let d in data) {
      ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    }
    return ret.join('&');
  };

  $('#contact-form').submit(function(event) {
    event.preventDefault();
    console.log($(this).serialize());

    const url = '/contact?' + $(this).serialize();
    $.post(url, {}, function(data){
      console.log(data);
    });
    return false;
  });

  const hash = window.location.hash;
  if (hash != null && hash.length > 0) {
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 500);
  }
});
