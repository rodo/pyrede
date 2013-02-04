/*
 * 
 * 
 * 
 * 
 */

function detect(vars, dist_id) {

    for (var elem in vars ) {

	url = '/json/pypi/'+vars[elem][0]+'/';

	fetch(url, dist_id, vars[elem][0]);
    }
    
}	      

function fetch(url, dist_id, elem) {
    $.get(url,
	  function(data) {

	      if (data.result == 1) {
		  $('#span_'+elem).addClass("badge badge-success");
	      } else {
		  if (data.nb_alt == 0) {
		      msg = 'unknown in pyrede db';
		      $('#provide_'+elem).html(msg);
		  } else if (data.nb_alt == 1) {
		      msg = 'did you mean <b>' + data.alt[0]['name'] + '</b> ?';
		      $('#provide_'+elem).html(msg);
		  } else {
		      $('#provide_'+elem).html('unknown in pyrede db');
		  }
		  $('#unofficial_'+elem).html('');
	      }

	      found = 0;

	      if (data.found > 0) {
		  
		  for (var pack in data.packages) {
		      if (data.packages[pack].distribution.id == dist_id) {
			  found = 1;
			  goodpack = data.packages[pack];
		      }

		      if (data.packages[pack].distribution.official == dist_id) {
			  unoffpack = data.packages[pack];
			  unoff = unoffpack.version;
			  $('#unofficial_'+elem).html('<b>'+unoff+'</b>');

			  $('#result_unoff').append(' '+unoffpack.name);
			  $('#result_unoff').css('visibility', 'visible');
		      }
		  }
	      }

	      if (found == 1) {
		  pr = goodpack.provide;

		  $('#provide_'+elem).html('<b>'+pr+'</b>');
		  $('#unofficial_'+elem).html();

		  $('#result').append(' '+goodpack.name);
		  $('#result_unoff').append(' '+goodpack.name);
		  $('#result').css('visibility', 'visible');
	      } else {
		  if (data.result == 1) {
		      text = 'nothing found';
		      $('#provide_'+elem).html(text);
		  }
	      }
	      if (data.result == 1) {
		  text = '<a class="btn btn-mini btn-primary" href="/pypi/'+elem+'/add/">add one</a>';
		  $('#button_'+elem).html(text);
	      }

	      
	  });
}
