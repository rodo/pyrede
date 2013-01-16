/*
 * 
 * 
 * 
 * 
 */

function detect(vars) {

    for (var elem in vars ) {

	url = '/json/pypi/'+vars[elem][0]+'/';

	fetch(url, vars[elem][0]);
    }
    
}	      

function fetch(url, elem) {
    $.get(url,
	  function(data) {

	      if (data.result == 1) {
		  $('#span_'+elem).addClass("badge badge-success");
	      } else {
		  $('#provide_'+elem).html('unknown in pyrede db');
	      }
	      if (data.found == 0) {
		  text = 'nothing found, <a href="/pypi/'+elem+'/add/">add one</a>';
		  $('#provide_'+elem).html(text);
	      }
	      if (data.found == 1) {
		  pr = data.packages[0].provide + ' ' + data.packages[0].distribution.name + ' ' + data.packages[0].distribution.version;
		  $('#provide_'+elem).html('<b>'+pr+'</b>');
		  $('#result').append('<span style="margin-left: 3px">'+data.packages[0].name+'</span>');
		  $('#result').css('visibility', 'visible');
	      }
	  });
}
