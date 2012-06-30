// BASE INCLUDE
phantom.injectJs( require('system').args[3].replace(/\/[^\/]*$/, '/lib/mwt.js') );



if( !casper.cli.has('search') || !casper.cli.has('url_pattern') || !casper.cli.has('desired_searchindex') )
{
	out( {'exception': true, 'success': false, 'message': 'Usage script.js --search=<search> --url_pattern=<url_pattern> --desired_searchindex=<desired_searchindex>'} );
}

var search = casper.cli.get('search');
var urlPattern = casper.cli.get('url_pattern');
var desiredIndex = casper.cli.get('desired_searchindex');


function findLink(urlPattern) {
	var lis = $('li.g');
	var idx = 0;
	for( var i = 0; i < lis.length; i++ )
	{
		idx++;
		var anchors = $(lis[i]).find('a');
		for( var j = 0; j < anchors.length; j++ )
		{
			var href = $(anchors[j]).attr('href');
			if( href && href.match(urlPattern) )
			{
				return idx;
			}
		}
	}
	return null;
}

var currentPage = 1;

var processPage = function() {
	var url;

	if( currentPage >= 5 )
	{
		out( {'success': false, 'searchIndex': 0, 'maxIndex': (10 * currentPage), 'args': {'search': search, 'url_pattern': urlPattern}} );
	}

	var searchIndex = this.evaluate(findLink, {urlPattern: urlPattern});
	if( searchIndex )
	{
        var realIdx = searchIndex * currentPage
		out( {'success': realIdx <= desiredIndex, 'searchIndex': realIdx, 'args': {'search': search, 'url_pattern': urlPattern}} );
	}

	if( this.exists("#pnnext") )
	{
		currentPage++;
		url = this.getCurrentUrl();
		this.thenClick("#pnnext").then(function() {
			this.waitFor(function() {
				return url !== this.getCurrentUrl();
			}, processPage, function() {
				out( {'exception': true, 'success': false, 'message': 'Google Timeout'}, 5000 );
			});
		});
	} else {
		out( {'success': false, 'searchIndex': 0, 'maxIndex': (10 * currentPage), 'args': {'search': search, 'url_pattern': urlPattern}} );
	}
};

casper.start('http://www.google.de/', function() {
	this.fill('form[action="/search"]', { q: search }, true);
});

casper.then(processPage);
casper.run(function() {
	this.exit();
});