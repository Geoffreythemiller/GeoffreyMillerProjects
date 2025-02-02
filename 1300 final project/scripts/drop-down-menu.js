$("#home-open").click(function() {
    $("#home-drop").removeClass("hidden");
    $("#home-close").removeClass("hidden");
    $("#bus-schedule-drop").addClass("hidden");
    $("#bus-schedule-close").addClass("hidden");
    $("#bus-stops-drop").addClass("hidden");
    $("#bus-stops-close").addClass("hidden");
    $("#tickets-drop").addClass("hidden");
    $("#tickets-close").addClass("hidden");
});

$("#bus-schedule-open").click(function() {
    $("#bus-schedule-drop").removeClass("hidden");
    $("#bus-schedule-close").removeClass("hidden");
    $("#home-drop").addClass("hidden");
    $("#home-close").addClass("hidden");
    $("#bus-stops-drop").addClass("hidden");
    $("#bus-stops-close").addClass("hidden");
    $("#tickets-drop").addClass("hidden");
    $("#tickets-close").addClass("hidden");
});

$("#bus-stops-open").click(function() {
    $("#bus-stops-drop").removeClass("hidden");
    $("#bus-stops-close").removeClass("hidden");
    $("#home-drop").addClass("hidden");
    $("#home-close").addClass("hidden");
    $("#bus-schedule-drop").addClass("hidden");
    $("#bus-schedule-close").addClass("hidden");
    $("#tickets-drop").addClass("hidden");
    $("#tickets-close").addClass("hidden");
});

$("#tickets-open").click(function() {
    $("#tickets-drop").removeClass("hidden");
    $("#tickets-close").removeClass("hidden");
    $("#home-drop").addClass("hidden");
    $("#home-close").addClass("hidden");
    $("#bus-schedule-drop").addClass("hidden");
    $("#bus-schedule-close").addClass("hidden");
    $("#bus-stops-drop").addClass("hidden");
    $("#bus-stops-close").addClass("hidden");
});

$("#home-close").click(function() {
    $("#home-drop").addClass("hidden");
});

$("#bus-schedule-close").click(function() {
    $("#bus-schedule-drop").addClass("hidden");
});

$("#bus-stops-close").click(function() {
    $("#bus-stops-drop").addClass("hidden");
});

$("#tickets-close").click(function() {
    $("#tickets-drop").addClass("hidden");
});

$(window).resize(function() {
    if ($(document).width() < 951) {
        $("#home-drop").addClass("hidden");
        $("#home-close").addClass("hidden");

        $("#bus-schedule-drop").addClass("hidden");
        $("#bus-schedule-close").addClass("hidden");

        $("#bus-stops-drop").addClass("hidden");
        $("#bus-stops-close").addClass("hidden");

        $("#tickets-drop").addClass("hidden");
        $("#tickets-close").addClass("hidden");
    }
});
