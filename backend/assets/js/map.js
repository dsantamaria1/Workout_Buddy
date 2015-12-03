var stream_id = $('#stream_id').text();

var clickFunction = function(id) {
	return function(){
		$('#map_canvas').gmap('openInfoWindow',
		{ content : '<img src="/img?photo_id='+id+'" height="100" width="100">' }, this);
	};
};

var process = function(result) {
	// We need to bind the map with the "init" event otherwise bounds will be null
	var images = result['images'];
	$('#map_canvas').gmap({'zoom': 2, 'disableDefaultUI':true}).bind('init', function(evt, map) {
		for ( var i = 0; i < images.length; i++ ) {

			$('#map_canvas').gmap('addMarker', {
				'position': new google.maps.LatLng(images[i].lat, images[i].lng)
			}).mouseover(clickFunction(images[i].image)).mouseout(function(){
				$('#map_canvas').gmap('closeInfoWindow');
			});

		}
		$('#map_canvas').gmap('set', 'MarkerClusterer', new MarkerClusterer(map, $(this).gmap('get', 'markers')));
	});
};

var update = function(result){
	var images = result['images'];
	$('#map_canvas').gmap('clear', 'markers');
	
	for ( var i = 0; i < images.length; i++ ) {
		$('#map_canvas').gmap('addMarker', {
			'position': new google.maps.LatLng(images[i].lat, images[i].lng)
		}).mouseover(clickFunction(images[i].image)).mouseout(function(){
			$('#map_canvas').gmap('closeInfoWindow');
		});

	}
	$('#map_canvas').gmap({ 'callback': function(map) {
		$('#map_canvas').gmap('set', 'MarkerClusterer', new MarkerClusterer(map, $(this).gmap('get', 'markers')));
	}});
};

var formatDate = function (d) {
 var date = new Date();
 date.setDate(date.getDate() + d);
 return date.toDateString().slice(4);
}

$( "#slider-range" ).slider({
  range: true,
  min: -365,
  max: 0,
  values: [ -365, 0 ],
  stop: function( event, ui ) {
		var start_time = formatDate(ui.values[ 0 ]);
		var end_time = formatDate(ui.values[ 1 ]);

    $( "#date" ).val(start_time + " - " + end_time);
		$.ajax({url: "/api/range?stream_id=" + stream_id + "&start_time=" + start_time + "&end_time=" + end_time, dataType:"json", success: update});
  }
});

$( "#date" ).val( formatDate($( "#slider-range" ).slider( "values", 0 )) +
  " - " + formatDate($( "#slider-range" ).slider( "values", 1 ) ));
$.ajax({url: "/api/range?stream_id=" + stream_id + "&start_time=" + formatDate($( "#slider-range" ).slider( "values", 0 ))
 + "&end_time=" + formatDate($( "#slider-range" ).slider( "values", 1 )), dataType:"json", success: process});
