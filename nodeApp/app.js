const irisnative = require('intersystems-iris-native')
const fs = require('fs')


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
  

  // Create Iris native onbject to call class methods through the native API
  const Iris = connection.createIris()

  // ***********************************************************************
  // Paste code here


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

