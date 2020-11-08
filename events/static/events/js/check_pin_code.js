function CheckPinCode(event, event_id, elem_html_id, pin_html_id) {
  var request = new XMLHttpRequest();
  var base_url = '/ajax/check_pin_code/?'
  var pin = document.getElementById(pin_html_id).value
  var url = base_url + 'pin=' + pin + '&event_id=' + event_id
  request.open('GET', url, true);

  request.onload = function() {
    if (this.status >= 200 && this.status < 400) {
      var resp = this.response;
      document.getElementById(elem_html_id).innerHTML = resp;
    }
  };

  request.send();
};

function foo(value) {
    console.log(value)
};