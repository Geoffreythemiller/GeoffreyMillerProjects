$("#plymouth-thumbnail").click(function() {
    $("#plymouth").removeClass("hidden");
    $("#amtrak-walk").addClass("hidden");
    $("#jfk-blvd").addClass("hidden");
    $("#bus-stop-area-2").addClass("hidden");
    $("#bus-stop-area").addClass("hidden");
    $("#kop-stop").addClass("hidden");

    $("#plymouth-thumbnail").addClass("thumbnail-clicked");
    $("#amtrak-walk-thumbnail").removeClass("thumbnail-clicked");
    $("#jfk-blvd-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-2-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-thumbnail").removeClass("thumbnail-clicked");
    $("#kop-stop-thumbnail").removeClass("thumbnail-clicked");
  });

$("#amtrak-walk-thumbnail").click(function() {
    $("#amtrak-walk").removeClass("hidden");
    $("#plymouth").addClass("hidden");
    $("#jfk-blvd").addClass("hidden");
    $("#bus-stop-area-2").addClass("hidden");
    $("#bus-stop-area").addClass("hidden");
    $("#kop-stop").addClass("hidden");

    $("#amtrak-walk-thumbnail").addClass("thumbnail-clicked");
    $("#plymouth-thumbnail").removeClass("thumbnail-clicked");
    $("#jfk-blvd-thumbnail").removeClassClass("thumbnail-clicked");
    $("#bus-stop-area-2-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-thumbnail").removeClass("thumbnail-clicked");
    $("#kop-stop-thumbnail").removeClass("thumbnail-clicked");
});

$("#jfk-blvd-thumbnail").click(function() {
    $("#jfk-blvd").removeClass("hidden");
    $("#plymouth").addClass("hidden");
    $("#amtrak-walk").addClass("hidden");
    $("#bus-stop-area-2").addClass("hidden");
    $("#bus-stop-area").addClass("hidden");
    $("#kop-stop").addClass("hidden");

    $("#jfk-blvd-thumbnail").addClass("thumbnail-clicked");
    $("#plymouth-thumbnail").removeClass("thumbnail-clicked");
    $("#amtrak-walk-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-2-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-thumbnail").removeClass("thumbnail-clicked");
    $("#kop-stop-thumbnail").removeClass("thumbnail-clicked");
});

$("#bus-stop-area-2-thumbnail").click(function() {
    $("#bus-stop-area-2").removeClass("hidden");
    $("#plymouth").addClass("hidden");
    $("#amtrak-walk").addClass("hidden");
    $("#jfk-blvd").addClass("hidden");
    $("#bus-stop-area").addClass("hidden");
    $("#kop-stop").addClass("hidden");

    $("#bus-stop-area-2-thumbnail").addClass("thumbnail-clicked");
    $("#plymouth-thumbnail").removeClass("thumbnail-clicked");
    $("#amtrak-walk-thumbnail").removeClass("thumbnail-clicked");
    $("#jfk-blvd-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-thumbnail").removeClass("thumbnail-clicked");
    $("#kop-stop-thumbnail").removeClass("thumbnail-clicked");
});

$("#bus-stop-area-thumbnail").click(function() {
    $("#bus-stop-area").removeClass("hidden");
    $("#plymouth").addClass("hidden");
    $("#amtrak-walk").addClass("hidden");
    $("#jfk-blvd").addClass("hidden");
    $("#bus-stop-area-2").addClass("hidden");
    $("#kop-stop").addClass("hidden");

    $("#bus-stop-area-thumbnail").addClass("thumbnail-clicked");
    $("#plymouth-thumbnail").removeClass("thumbnail-clicked");
    $("#amtrak-walk-thumbnail").removeClass("thumbnail-clicked");
    $("#jfk-blvd-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-2-thumbnail").removeClass("thumbnail-clicked");
    $("#kop-stop-thumbnail").removeClass("thumbnail-clicked");
});

$("#kop-stop-thumbnail").click(function() {
    $("#kop-stop").removeClass("hidden");
    $("#plymouth").addClass("hidden");
    $("#amtrak-walk").addClass("hidden");
    $("#jfk-blvd").addClass("hidden");
    $("#bus-stop-area-2").addClass("hidden");
    $("#bus-stop-area").addClass("hidden");

    $("#kop-stop-thumbnail").addClass("thumbnail-clicked");
    $("#plymouth-thumbnail").removeClass("thumbnail-clicked");
    $("#amtrak-walk-thumbnail").removeClass("thumbnail-clicked");
    $("#jfk-blvd-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-2-thumbnail").removeClass("thumbnail-clicked");
    $("#bus-stop-area-thumbnail").removeClass("thumbnail-clicked");
});
