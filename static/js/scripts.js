$(function () {
  var textfield = $("input[name=user]");
  $('button[type="submit"]').click(function (e) {
    e.preventDefault();

    //little validation just to check username

    if (textfield.val() != "") {
      //$("body").scrollTo("#output");
      $("#output")
        .addClass("alert alert-success animated fadeInUp")
        .html(
          "Welcome back " +
            "<span style='text-transform:uppercase'>" +
            textfield.val() +
            "</span>"
        );
      $("#output").removeClass(" alert-danger");
      $("input").css({
        height: "0",
        padding: "0",
        margin: "0",
        opacity: "0",
      });
    } else {
      //remove success mesage replaced with error message
      $("#output").removeClass(" alert alert-success");
      $("#output")
        .addClass("alert alert-danger animated fadeInUp")
        .html("sorry enter a username ");
    }
    //console.log(textfield.val());
  });
});
