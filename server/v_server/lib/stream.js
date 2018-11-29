var fs = require('fs');
var url = require('url');
var querystring = require('querystring');
var path = require('path');

var cf = require('../cf/cf');
var mime = {
    html: 'text/html',
    txt: 'text/plain',
    css: 'text/css',
    gif: 'image/gif',
    jpg: 'image/jpeg',
    png: 'image/png',
    svg: 'image/svg+xml',
    js: 'application/javascript'
};

function serveWithRanges(request, response, file) {
    var range = request.headers.range;
    //var total = content.length;
    if(range) {
        var parts = range.replace(/bytes=/, "").split("-");
        var partialstart = parts[0];
        var partialend = parts[1];
    }

    var stats = fs.statSync(file);
    var start_r = partialstart ? parseInt(partialstart, 10) : 0;
    //var end = partialend ? parseInt(partialend, 10) : start + cf.limit - 1;
    var end = partialend ? parseInt(partialend, 10) : stats.size - 1;
    end = end > stats.size - 1 ? stats.size - 1 : end;
    var chunksize = end - start_r + 1;
    //var chunksize = stats.size;
    response.writeHead(206, {
        "Content-Range": "bytes " + start_r + "-" + end + "/" + stats.size,
        "Accept-Ranges": "bytes",
        "Content-Length": chunksize,
        "Content-Type": "video/mp4"
    });

    var rs = fs.createReadStream(file, {start: start_r});
    var stream = rs.pipe(response);
    stream.on('error', err => {
        console.log(err)
        response.writeHead(400, { "Content-Type": "text/plain" });
    });
    stream.on('end', () => {
        response.end();
    });

    stream.on('finish', () => {
        response.end();
    });
    //fs.open(file, 'r', function(err, fd){
    //    console.log('openfile', file);
    //    var readBuffer = new Buffer(chunksize);
    //    var len = chunksize;
    //    var offset = 0;
    //    var filePostion = start;
    //    fs.read(fd, readBuffer, offset, len, filePostion, function(err, readByte, readResult){
    //        if(err) {
    //        	console.log(err,'xxx');
    //        }
    //        response.end(readBuffer); 
    //        fs.close(fd, err => {
    //            if(err) {
    //                console.log(err);
    //            }
    //        });
    //    });
    //});
}

function serveCover(request, response, file) {
    if(file && file.indexOf('..') != -1) {
        response.writeHead(400);
        response.end("<h1>400, not found.</h1>");       
	return;
    }
    var type = mime[path.extname(file).slice(1)];
    var stats = fs.statSync(file);
    var total = stats.size;
    if (type) {
        response.writeHead(200, { 
            "Content-Type": type,
            "Content-Length": total
        });
        //response.end(content);
    }
    else {
        response.writeHead(401, { "Content-Type": "text/plain" });
        response.end('401 Not Found');
    }
    var rs = fs.createReadStream(file);
    var stream = rs.pipe(response);
    stream.on('error', err => {
        console.log(err)
        response.writeHead(400, { "Content-Type": "text/plain" });
    });
    stream.on('end', () => {
        response.end();
    });
    stream.on('finish', () => {
        response.end();
    });
}

function serveWithoutContentLength(request, response, content) {
    response.writeHead(200, {
        "Content-Type": "audio/ogg"
    });
    response.end(content);
}

function serveWithoutRanges(request, response, content) {
    var total = content.length;
    var start = 0;
    var end = 0;
    var chunksize = 0;
    start = 0;
    end = content.length - 1;
    if (request.url.match(".ogg$")) {
        response.writeHead(200, { 
            "Content-Type": "audio/ogg",
            "Content-Length": end
        });
    }
    else {
        response.writeHead(200, { "Content-Type": "text/html" });
    }
    response.end(content);
}

function serveHTML(request, response, content) {
    response.writeHead(200, 
        {"Content-Type": "text/html"},
        {"Content-Length": content.length}
    );
    response.end(content);
}

function readcontent(callback, request, response) {
    var myurl = url.parse(request.url);
    var filename = querystring.parse(myurl.query).file;
    if(filename && filename.indexOf('..') != -1) {
        response.writeHead(400);
        response.end("<h1>400, not found.</h1>");       
	return;
    }
    var definition = querystring.parse(myurl.query).definition;
    var version = querystring.parse(myurl.query).version;
    var file =  cf.video_path + '/' + version + '/' + definition + '/' + filename;
    console.log(file);
    fs.stat(file, (err, stat) => {
        if (err) {
          response.writeHead(400);
          response.end("<h1>404, not found.</h1>");
        }
        else {
            if (!stat.isFile()) {
                response.writeHead(400);
                response.end("<h1>404, not found.</h1>");
            }
            else {
                callback(request, response, file);
            }
        }
    });
}

function readJpgContent(callback, request, response) {
    var path_map = {
        'icon' : 'icon_path',
        'cover' : 'cover_path',
        'qr' : 'qr_path'
    }
    var myurl = url.parse(request.url);
    var pathname = myurl.pathname;
    if(pathname && pathname.indexOf('..') != -1) {
        response.writeHead(400);
        response.end("<h1>400, not found.</h1>");       
	return;
    }
    var filename = querystring.parse(myurl.query).file;
    if(filename && filename.indexOf('..') != -1) {
        response.writeHead(400);
        response.end("<h1>400, not found.</h1>");       
	return;
    }
    var path = path_map[pathname.slice(1)];
    if(!path) {
        response.writeHead(404);
        response.end("<h1>404, not found.</h1>");
        return;
    }

    var file =  cf[path] + '/' + filename;
    console.log(file);
    fs.stat(file, (err, stat) => {
        if (err) {
            response.writeHead(404);
            response.end("<h1>404, not found.</h1>");
        }
        else {
            if (!stat.isFile()) {
                response.writeHead(404);
                response.end("<h1>404, not found.</h1>");
            }
            else {
                callback(request, response, file);
            }
        }
    });
}

module.exports = {
    readcontent : readcontent,
    readJpgContent : readJpgContent,
    serveWithRanges : serveWithRanges,
    serveCover : serveCover
}
