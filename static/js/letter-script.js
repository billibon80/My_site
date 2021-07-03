$(document).ready(function() {
    $("#letterOpenButton").click(function(e) {
        e.preventDefault();
        $("#letter>.message").eq(0).addClass("active");
    });
 $("#letterCloseButton").click(function(e) {
        e.preventDefault();
        $("#letter>.message").removeClass("active");
    });
});
