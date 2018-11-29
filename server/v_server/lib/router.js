var stream = require('./stream.js');

var router = {
    // normal response
    "/ranges" : function(request, response) {
        stream.readcontent(stream.serveWithRanges, request, response);
    },
    "/qr" : function(request, response) {
        stream.readJpgContent(stream.serveCover, request, response);
    },
    "/icon" : function(request, response) {
        stream.readJpgContent(stream.serveCover, request, response);
    },
    "/cover" : function(request, response) {
        stream.readJpgContent(stream.serveCover, request, response);
    }
};

module.exports = router;
