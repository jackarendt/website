String.prototype.format = function() {
  var content = this;
  for (let i = 0; i < arguments.length; i++) {
    var replacement = ('{' + i + '}').replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    content = content.replace(RegExp(replacement, 'g'), arguments[i]);
  }
  return content
}

// Add on click handlers for buttons.
$(document).ready(function() {
  $('#contact-form').submit(function(event) {
    event.preventDefault();
    const url = '/contact?' + $(this).serialize();
    $.get(url, function(data, status) {
      if (status !== 'success') {
        return;
      }

      let dataJSON = JSON.parse(data);
      var responseClass = 'form-error';
      if (dataJSON.success) {
        $('#contact-form').find('input[type=text], textarea').val('');
        responseClass = 'form-success';
      }

      const html = `
        <p class='form-response {0}' id='formResponse'>{1}</p>
      `.format(responseClass, dataJSON.message);

      $(html).hide().insertAfter($('#contact-form')).fadeIn('fast');

      setTimeout(function(){
        $('#formResponse').fadeOut('fast', function() {
          $(this).remove();
        })
      }, 2000);
    });
    return true;
  });

  const hash = window.location.hash;
  if (hash != null && hash.length > 0) {
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 500);
  }
});
