var jsPath = 'js/';

var system = require('system');
for( sys in system.args )
{
	var m = system.args[sys].match(/^(.+)google_search_index\.js$/);
	if( m )
	{
		jsPath = m[1];
	}
}

var casper = require("casper").create({
	clientScripts: [
		jsPath + 'jquery-1.7.1.min.js'
	],
	logLevel: 'info',
	pageSettings: {
		'userAgent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.43 Safari/536.11"
	},
	viewportSize: {width: 800, height: 600},
	onError: function(self, msg) {
		out( {'success': false, 'message': msg} );
	}
});

function out(obj)
{
	console.log( JSON.stringify(obj) );
	casper.exit();
}

if( !casper.cli.has(1) )
{
	out( {'success': false, 'message': 'Usage script.js <search> <urlPattern>'} );
}

var search = casper.cli.get(0);
var urlPattern = casper.cli.get(1);

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
		out( {'success': true, 'searchIndex': 0, 'maxIndex': (10 * currentPage), 'args': {'search': search, 'urlPattern': urlPattern}} );
	}

	var searchIndex = this.evaluate(findLink, {urlPattern: urlPattern});
	if( searchIndex )
	{
		out( {'success': true, 'searchIndex': (searchIndex * currentPage), 'args': {'search': search, 'urlPattern': urlPattern}} );
	}

	if( this.exists("#pnnext") )
	{
		currentPage++;
		url = this.getCurrentUrl();
		this.thenClick("#pnnext").then(function() {
			this.waitFor(function() {
				return url !== this.getCurrentUrl();
			}, processPage, function() {
				out( {'success': false, 'message': 'Google Timeout'}, 5000 );
			});
		});
	} else {
		out( {'success': true, 'searchIndex': 0, 'maxIndex': (10 * currentPage), 'args': {'search': search, 'urlPattern': urlPattern}} );
	}
};

casper.start('http://www.google.de/', function() {
	this.fill('form[action="/search"]', { q: search }, true);
});

casper.then(processPage);
casper.run(function() {
	this.exit();
});