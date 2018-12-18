// JavaScript file to autopopulate donor and donation information
// based off of dropdowns on submit donation page

/* global $ */
/* global jQuery */


$('#existing-donor-button').click(function () {
    var id = $('#existing-donor option:selected').data("id");
    var type = $('#existing-donor option:selected').data("category");
    var phone = $('#existing-donor option:selected').data("phone");
    var email = $('#existing-donor option:selected').data("email");
    var address = $('#existing-donor option:selected').data("address");
    var description = $('#existing-donor option:selected').data("description");

    $("#existing-id").text(id);
    $("#existing-category").text(type);
    $("#existing-phone").text(phone);
    $("#existing-email").text(email);
    $("#existing-address").text(address);
    $("#existing-description").text(description);
});


$('#existing-donation-button').click(function () {
  var units = $('#existing-donation option:selected').data("units");
  var category = $('#existing-donation option:selected').data("category");
  console.log($('#existing-donation').val());
  console.log(units);
  console.log(category);
  $("#existing-units").text(units);
  $("#ex-category").text(category);
  
});
