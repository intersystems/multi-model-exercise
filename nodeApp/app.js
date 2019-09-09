const irisnative = require('intersystems-iris-native')
const http = require('http')
const port = 8080
const ip = require("ip");
const fs = require('fs')
const url = require('url');
const querystring = require('querystring');






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
  
  
  console.log("connection to Iris...")
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

          //call the classmethod in the Employee class (inherited from the JSONMaker superclass)
          Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(body))
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

function getConnectionsConfig() {
  data = fs.readFileSync("../connections.config", "utf8")
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

