$(document).ready(function() {
  $.ajax('/numbers_files').done(function(result) {
    var numbers_files = result['numbers_files'];
    for (i = 0; i < numbers_files.length; i++) {
      $("#numbersFileSelect").append($("<option></option>").attr("value", numbers_files[i]).text(numbers_files[i]));
    }
  });

  $("#numbersFileSelect").on('change', function() {
    var number_file = this.value;
    $("#numbersContainer").slideUp(function() {
      if (number_file == "placeholder") return;

      $.ajax('/numbers?file=' + number_file).done(function(result) {
        var numbers = result['numbers'];
        $("#numbers").empty();
        for (i = 0; i < numbers.length; i++) {
          var number_elem = $("<p>").addClass('numberContainer');
          number_elem.append($("<span>").text(numbers[i] + " ").attr('class', 'number'));
          number_elem.append($("<a>").attr('href', '#').text("(delete)").attr('class', 'deleteLink'));
          number_elem.appendTo($("#numbers")).show('slow');
        }

        $("#numbersContainer").slideDown();
      });
    });
  });

  $("#sendMessageForm").on('submit', function(e) {
    var messageBody = $("#messageBody").val();
    e.preventDefault();
    $.post('/send_sms', { file: $("#numbersFileSelect").val(), message_body: messageBody }).done(function(data) {
      $("#messageBody").attr('val', '');
      alert("Message sent to all numbers in " + $("#numbersFileSelect").val());
    });
  });

  $("#addNumberForm").on('submit', function(e) {
    var newNumber = $("#newNumber").val();
    e.preventDefault();
    $.post('/add_number', { file: $("#numbersFileSelect").val(), number: newNumber }).done(function(data) {
      var number_elem = $("<p>").addClass('numberContainer');
      number_elem.append($("<span>").text(newNumber + " ").attr('class', 'number'));
      number_elem.append($("<a>").attr('href', '#').text("(delete)").attr('class', 'deleteLink'));
      $("#numbers").append(number_elem);
      $("#newNumber").val('');
    }).error(function(data) {
      alert("That phone number already exists.");
    });
  });

  $('body').on('click', 'a.deleteLink', function() {
    var number = $(this).siblings('.number').text();
    var numberContainer = $(this).parent('.numberContainer');
    $.post('/delete_number', { file: $("#numbersFileSelect").val(), number: number }).done(function(data) {
      numberContainer.slideUp();
    });
  });
});
