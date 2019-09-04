const irisnative = require('intersystems-iris-native')

var http = require('http');

var ip = require("ip");
console.dir ( ip.address() );

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World!');
}).listen(8080);