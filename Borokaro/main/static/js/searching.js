$( function() {
    var availableTags = []
    $.ajax({
      method: "GET",
      url: "/productlist",
      success: function(response) {
        // console.log(response);
        startAutoComplete(response);
      }
    });

    function startAutoComplete(availableTags){
      $( "#searchProduct" ).autocomplete({
        source: availableTags
      });
    }

  } );