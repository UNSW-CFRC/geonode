co2_now = 0;

$(window).load(init_co2);

function init_co2() {
  co2_now = read_co2();
  $('#myRange').val(co2_now);
  _display_CO2(co2_now);
}

function read_co2() {
  return 420;
}

function _display_CO2(value) {
  $('#val').html(value + ' ppm');

  if (value < 600) {
      $('#valText').html('very good');
    } else if (value < 1000) {
      $('#valText').html('good');
    } else if (value < 1400) {
      $('#valText').html('fair');
    } else if (value < 1800) {
      $('#valText').html('poor');
    } else  {
      $('#valText').html('very poor');
    }

  hue = (2200 - value) / 1800 * 80;
  color = 'hsla(' + hue + ', 42%, 54%, 1)'
  $('#squiggle').css('backgroundColor', color);
  $('#valText').css('color', color);
}

$('#myRange').on('input', function() {
  _display_CO2(this.value);
});

$( "#myRange" ).on('touchend mouseup', function() {
  console.log('touchend mouseup');
  $('#myRange').val(co2_now);
  _display_CO2(co2_now);
});
