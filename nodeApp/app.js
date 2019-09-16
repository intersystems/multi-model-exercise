const irisnative = require('intersystems-iris-native')
const http = require('http')
const ip = require("ip");
const fs = require('fs')
const url = require('url');
const querystring = require('querystring');
const port = 8080


function main() 
{
  preConfig = getConnectionsConfig()
  const connectionConfig = {
    host : preConfig['ip'], 
    port : parseInt(preConfig['port']),
    ns : preConfig["namespace"],
    user : preConfig["username"],
    pwd : preConfig['password']
  }
  
  
  console.log("connecting to InterSystems IRIS...")
  const connection = irisnative.createConnection(connectionConfig)
  console.log("Connected to InterSystems IRIS.")
  console.dir ( ip.address() + ":" + port);

  //create Iris native onbject to call class methods through the native API
  const Iris = connection.createIris()

  http.createServer(function (req, res) {
    var q = url.parse(req.url);

    if (q.pathname =="/submit") {
      let body = '';
      req.on('data', chunk => {
          body += chunk.toString(); // convert Buffer to string
      });
      req.on('end', () => {
          //parsing the urlencoded form data
          body = querystring.parse(body)

        //Your code here
        
          res.end('Thank You');
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

function getConnectionsConfig() {
  data = fs.readFileSync("../connections.config", "utf8")
  data = data.trim()
  data = data.split("\n")
  config = {}
  for (line of data) {
    line = line.split(":")
    if (line[0] == "driver"){continue}
    config[line[0].trim()] = line[1].trim()
  }
  return config
}

main()

