$('#val').html($('#myRange').value);

$('#myRange').on('input', function() {
  $('#val').html(this.value);

  if (this.value < 600) {
      $('#valText').html('very good');
    } else if (this.value < 1000) {
      $('#valText').html('good');
    } else if (this.value < 1400) {
      $('#valText').html('fair');
    } else if (this.value < 1800) {
      $('#valText').html('poor');
    } else  {
      $('#valText').html('very poor');
    }

  hue = (2200 - this.value) / 1800 * 80;
  color = 'hsla(' + hue + ', 42%, 54%, 1)'
  $('#squiggle').css('backgroundColor', color);
  $('#valText').css('color', color);
});
