
$("#search").blur(function () {
  setTimeout(function () {
    $("#search-results").css("display", "none");
  }, 200);
});


$("#search").on("input", function (e) {

    console.log($("#search").val().length);
    if ($("#search").val().length >= 3) {
        $("#search-results").css("display", "block");
    } else {
        $("#search-results").css("display", "none");
        return;
    }
  var query = $(this).val();

  $.ajax({
    url: "/search?q=" + query,
    success: function (results) {
      $("#search-results").empty();
      for (var i = 0; i < Math.min(results.length, 5); i++) {
        var result = results[i];
        var resultElement = $(
          '<a href="/recipe/' +
            result.key +
            '" class="list-group-item list-group-item-action">' +
            result.name +
            "</a>"
        );
        $("#search-results").append(resultElement);
      }
    },
  });
});
$("#search").on('keyup', function (e) {
    if (e.key === 'Enter' || e.keyCode === 13) {
        var query = $(this).val();
        window.location.href = "/search?p=html&q=" + query;
    }
});