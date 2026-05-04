$("#north-campus-thumbnail").click(function() {
    $("#north-campus").removeClass("hidden");
    $("#west-campus").addClass("hidden");
    $("#ithaca-college").addClass("hidden");

    $("#north-campus-thumbnail").addClass("thumbnail-clicked");
    $("#west-campus-thumbnail").removeClass("thumbnail-clicked");
    $("#ithaca-college-thumbnail").removeClass("thumbnail-clicked");
  });

$("#west-campus-thumbnail").click(function() {
    $("#west-campus").removeClass("hidden");
    $("#north-campus").addClass("hidden");
    $("#ithaca-college").addClass("hidden");

    $("#west-campus-thumbnail").addClass("thumbnail-clicked");
    $("#north-campus-thumbnail").removeClass("thumbnail-clicked");
    $("#ithaca-college-thumbnail").removeClass("thumbnail-clicked");
});

$("#ithaca-college-thumbnail").click(function() {
    $("#ithaca-college").removeClass("hidden");
    $("#north-campus").addClass("hidden");
    $("#west-campus").addClass("hidden");
    
    $("#ithaca-college-thumbnail").addClass("thumbnail-clicked");
    $("#north-campus-thumbnail").removeClass("thumbnail-clicked");
    $("#west-campus-thumbnail").removeClass("thumbnail-clicked");
});
