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
		  $('#provide_'+elem).html('unknown in pyrede db');
	      }

	      found = 0;

	      if (data.found == 1) {
		  
		  for (var pack in data.packages) {
		      if (data.packages[pack].distribution.id == dist_id) {
			  found = 1;
			  goodpack = data.packages[pack];
		      }
		  }
	      }

	      if (found == 1) {
		  pr = goodpack.name + ' ' + goodpack.provide;
		  $('#provide_'+elem).html('<b>'+pr+'</b>');
		  $('#result').append('<span style="margin-left: 3px">'+goodpack.name+'</span>');
		  $('#result').css('visibility', 'visible');
	      } else {
		  text = 'nothing found, <a href="/pypi/'+elem+'/add/">add one</a>';
		  $('#provide_'+elem).html(text);
	      }
	  });
}
