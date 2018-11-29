var http = require('http');
var path = require('path');
var url = require('url');

var cf = require('./cf/cf');
var router = require('./lib/router');

http.createServer(function (request, response) {
    var myurl = url.parse(request.url);
    console.log(myurl.pathname);
    var func = router[myurl.pathname];
    if (func !== undefined) {
        func(request, response);
    }
    else {
        console.log(404);
        response.writeHead(404);
        response.end("404, not found.");
    }
}).listen(cf.port);

console.log('Server running at port:', cf.port);
