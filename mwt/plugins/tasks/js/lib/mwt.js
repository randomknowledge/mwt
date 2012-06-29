var BASEDIR = require('system').args[3].replace(/\/[^\/]*$/, '');

var casper = require("casper").create({
	clientScripts: [
		BASEDIR + '/lib/jquery-1.7.1.min.js'
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