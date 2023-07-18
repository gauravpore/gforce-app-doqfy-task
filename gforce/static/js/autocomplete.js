$(document).ready(function () {
  $("#search-input").on("input", function () {
    var query = $(this).val();

    $.ajax({
      url: "/get-country-data/",
      type: "GET",
      data: { query: query },
      success: function (data) {
        // Handle the auto-suggest response
        var suggestions = data.suggestions;
        // Update the auto-suggest dropdown or perform other actions
      },
      error: function (error) {
        console.error(error);
      },
    });
  });
});
