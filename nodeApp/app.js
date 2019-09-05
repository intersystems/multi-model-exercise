const irisnative = require('intersystems-iris-native')
const http = require('http')
const port = 8080
const ip = require("ip");
const fs = require('fs')
const url = require('url');
const querystring = require('querystring');


console.dir ( ip.address() );



function main() 
{
  var ip = "104.154.144.38"
  var port = 25404
  var namespace = "USER"
  var username = "SuperUser"
  var password = "SYS"
  
  console.log("connection to Iris...")
  const connection = irisnative.createConnection({host: ip, port: port, ns: namespace, user: username, pwd: password})
  console.log("Hello World! You have successfully connected to InterSystems IRIS.")

  const Iris = connection.createIris()

  schemaTest = {
    "Name": "Duong2",
    "Title" : "Technical Course Developer",
    "Department": "Learning Services"
  }
  
  
  // status = Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(schemaTest))
  // console.log(status)




  http.createServer(function (req, res) {
    var q = url.parse(req.url);
    if (q.pathname =="/submit") {
      
      let body = '';
      req.on('data', chunk => {
          body += chunk.toString(); // convert Buffer to string
      });
      req.on('end', () => {
          body = querystring.parse(body)
          Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(body))
          console.log(body);
          res.end('ok');
      })
    }
    else {
    fs.readFile('static/index.html', function (err, data) {
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data)
      res.end();
    }) 
  }
  }).listen(8080);
}

main()
