# Multi-Model Exercise

This exercise details the process of using InterSystems IRIS® data platform multi-model capability to create a Node.js application that  sends JSON data straight to your database instance without any parsing or mapping.

In this exercise, we will use Python, JavaScript, and InterSystems ObjectScript to interact with data from different contexts, following these steps:

1. Use Python to create a table schema using standard SQL statements.
2. Modify the underlying ObjectScript class for that table to allow it to receive and persist JSON data directly.
3. Create a simple Node.js application that will send JSON files to the instance of InterSystems IRIS.
4. Query that database using Python again to see how the same data could be accessed in multiple languages from multiple contexts.

## Installation steps

1. Open the InterSystems IRIS sandbox IDE and clone this repository: `git clone -b try-iris https://github.com/intersystems/multi-model-exercise`.

3. Open the connections.config file in the top-level directory and update the IP and Port fields to match the ‘Server IP Address’ and 'Server Port' fields found in your sandbox and click save.

## Create The Table Schema Using Python

1. Install and configure Python
  	* Run `cd ~/multi-model-exercise/python`
	* Run `odbcinst -i -d -f pyodbc_wheel/linux/odbcinst.ini`
	
		
2. Open `python/createSchema.py` and scroll down to the `create_employee` function. Below the function declaration, uncomment the following code:

	```python
	create_employee = """
		CREATE TABLE Demo.Employee(
		    ID Integer PRIMARY KEY AUTO_INCREMENT,
		    Name varchar(256),
		    Title varchar(256), 
		    Department varchar(50)
		)
	    """
	```

	As you can see, this is a standard SQL create statement that will generate an Employee table on your InterSystems IRIS instance.
	

3. Run `python createSchema.py`. If successful, the terminal will output `Created table Demo.Employee successfully`.
   
	
4. Confirm that the `Demo.Employee` table has been created.
   1. Open the Management Portal by clicking **InterSystems** > **Management Portal** at the top of your sandbox IDE.
   3. Navigate to **System Explorer > SQL** and expand the **Tables** section. Find `Demo.Employee` in the list.

## Modify the table class using InterSystems ObjectScript

### Setting Up the Visual Studio Code ObjectScript Extension

1. [Install InterSystems Visual Studio Code](https://code.visualstudio.com/), if you have not already done so.
2. Open Visual Studio code. In the Extensions Manager, search for and install the `InterSystems ObjectScript` extension.
3. Select a folder for your workspace by selecting **Open Folder** in the File Explorer, or **File** > **Open**. Select or create a folder on your local machine to store settings specific to your workspace.
4. Open your Visual Studio Code settings (**File** (or **Code** if on macOS) > **Preferences** > **Settings** > **InterSystems ObjectScript**, select Workspace, then select **Edit in settings.json** (under "Objectscript: Conn"). Paste the following, filling in the settings for your InterSystems IRIS instance connection:
	```javascript
	{
		"objectscript.conn": {
			"active": true, 
			"label": "LOCAL",
			"host": "<ip for your instance>", // if using Sandbox, use the IDE Server Address
			"port": 80, // if using Sandbox, the IDE Server Port
			"username": "tech",
			"password": "demo",
			"ns": "USER", // the namespace you wish to connect to
			"https": false
		}
	}
	```

4. Navigate to the **ObjectScript: Explorer** pane by clicking on the InterSystems logo on the left side of your Visual Studio Code window, right-click `Classes/Demo/Employee.cls` and select **Export**.

5. Navigate to the **Explorer** pane and open the newly created `src/Demo/Employee.cls` file.

### Modifying Classes With Visual Studio Code

1. At the top of the Demo.Employee class, change `Extends %Persistent` to `Extends (%Persistent, %JSON.Adaptor)`. 

InterSystems ObjectScript is an object-oriented programming language that supports multiple inheritance.  This means that by inheriting the `%JSON.Adaptor` class, your table is now automatically able to import JSON data into instances. For more information on the `%JSON.Adaptor` class read [Using the JSON Adaptor](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GJSON_adaptor).

2. Because our table includes an auto-incremented primary key, we need to tell the `JSON.Adaptor` class not to look for that field in incoming JSON files, but to output it as a field when exporting class instances to JSON format.  To do this, find the ID property in the Employee class and add `(%JSONINCLUDE = "outputonly")` after `%Library.AutoIncrement`.
3. Before we can run this file, we need to add one small class method to expose the functionality of the `%JSON.Adaptor` class to the Native API (and, by extension, to our Node.js application).  Below the Property and Parameter declarations in the `Demo.Employee` class, paste the following code.

```ObjectScript
ClassMethod fromJSON(jsonString as %String) As %Status
{
	set employee = ..%New() 		//create a new class instance
	do employee.%JSONImport(jsonString) 	//call the %JSON.Adapter instance method to import JSON string
	set employee.ID = 0 			//this field must be set to 0 for the %Library.AutoIncrement class to increment correctly
	set status =  employee.%Save() 		//this persists the instance

	return status
}
```

1. Make sure to recompile the `Demo.Employee` class by saving it. You have now configured your SQL table class to receive JSON data and automatically create a new record from it. 

Note: The completed ObjectScript `Employee` class is included in this repository for your reference at `ObjectScript/Demo.Employee.cls`.

## Create A Node.js App to send JSON files to your database

2. Return to your InterSystems IRIS sandbox IDE and run `cd ~/multi-model-exercise/nodeApp`
3. Create a new file called `record.json` containing the following JSON object:

	```javascript
	{
		"Name": "JJ Smith",
		"Title": "Software Engineer",
		"Department": "Engineering"
	}
	```

4. Run `npm install --save intersystems-iris-native`. This installs the InterSystems IRIS Native API, which enables you to both access the underlying data structures in your database, and to call ObjectScript class methods directly from your code.
5. Open the `app.js` file. Navigate to `const Iris = connection.createIris()` and uncomment the following lines:

	```JavaScript
	let record = JSON.parse(fs.readFileSync("./record.json", "utf8"))
	Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(record))
	console.log(`Created new record in Demo.Employee table.`)
	```

	This code calls a class method using the Native API and passes a JSON string as a parameter. For more information, see [Calling ObjectScript Methods and Functions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=BJSNAT_call)
	
6. In the terminal, type `node app.js`. The node application will output that it has created a new record.

## Query The Database With Python

1. `cd` back into the Python directory (`cd ~/multi-model-exercise/python`)
2. Run `python query.py`. You should see the results of the SQL query, which includes the record of JJ Smith that you inserted using Node.js.

## Troubleshooting

Problem | Likely Solution 
------------------------- | ------------------------
My node.js app quits unexpectedly when I click **Submit**. | Make sure that you click **Save** in Visual Studio Code and that the class compiled successfully. 




