    $(document).ready(function() {
      var cache = {};
      $( "#searchTerm" ).autocomplete({
        minLength: 1,
        source: function( request, response ) {
          var term = request.term;
          if ( term in cache ) {
            response( cache[ term ] );
            return;
          }

          $.getJSON( "/api/autoComp", request, function( data, status, xhr ) {
            var upper_limit = 0;
            var data_post = [];
            if (data.length > 20){
              upper_limit = 20;
            }
            else{
              upper_limit = data.length
            }
            for(var i = 0; i < upper_limit; i++){
              data_post[i] = data[i];
            }
            cache[ term ] = data_post;
            response( data_post );
          });
        },
        select: function(event, ui) {
          var term_ = $('#searchTerm').text();
          //need to fill in input value
          $("input#searchTerm").val(ui.item.value);
          //$("#searchForm").submit();
          window.location.href = '/search?query=' + ui.item.value;
          //$.ajax({url: "/search?query=" + ui.item.value});
        }
      });
    });
