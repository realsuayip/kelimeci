$(document).ready(function($) {
    $(".clickable-tr").click(function() {
        window.location = $(this).data("href");
    });
});
