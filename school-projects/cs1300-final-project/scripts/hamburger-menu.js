$("#hamburger-menu").click(function() {
  if ($("#hamburger-navigation-menu").hasClass("hidden")) {
    $("#hamburger-navigation-menu").removeClass("hidden");
  } else {
    $("#hamburger-navigation-menu").addClass("hidden");
  }
});


$(window).resize(function() {
  if ($(document).width() < 951) {
      $("#hamburger-menu").removeClass("hidden");
      $("#drop-down-navigation-menu").addClass("hidden");
  } else {
      $("#hamburger-menu").addClass("hidden");
      $("#drop-down-navigation-menu").removeClass("hidden");
      $("#hamburger-navigation-menu").addClass("hidden");
  }
});


$(document).ready(function() {
  if ($(document).width() < 951) {
    $("#hamburger-menu").removeClass("hidden");
    $("#drop-down-navigation-menu").addClass("hidden");
  } else {
    $("#hamburger-menu").addClass("hidden");
    $("#drop-down-navigation-menu").removeClass("hidden");
  }
});
