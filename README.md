# Multi-Model Exercise

This exercise details the process of using InterSystems IRIS® data platform multi-model capability to create a Node.js application that  sends JSON data straight to your database instance without any parsing or mapping. 

In this exercise, we will use Python, JavaScript, and InterSystems ObjectScript to interact with data from different contexts, following these steps:
1.	Use Python to create a table schema using standard SQL statements.
2.  Modify the underlying ObjectScript class for that table to allow it to receive and persist JSON data directly.
3.  Create a simple Node.js application that will send JSON files to the instance of InterSystems IRIS. 
4.	Query that database using Python again to see how the same data could be accessed in multiple languages from multiple contexts.

## Installation steps:
It is recommended that you use the [InterSystems IRIS Sandbox](www.intersystems.com/try) to run this exercise. If you do so, skip the following installation steps and begin the exercise with step # "Title of Step".
1. This exercise requires the 64-bit version of Python 3.
	* If you already have Python installed, be sure to check what bit version you are using by launching the python shell by typing `python` .  If the version is 2, try quitting the shell (`control-z + enter` on Windows, or `control-d` on macOS) and typing `python3` .
	* Install Python by going here https://www.python.org/downloads/ (be sure to check off 'Add Python to environment variables' in the 'Advanced Options' section of the installation.

	* **Note**: do not click the 'Download Python 3.7.4' button directly on that site as it might download the 32 bit version of python, which will not work with the exercise. Select the link to your operating system and download the 64 bit Python file.
	* You may need to restart your terminal or even add python to the PATH environment variable if the python command does not work after installing python.

2. Open the InterSystems IRIS sandbox IDE. If you are completing this exercise on your local machine, open Visual Studio Code, which can be downloaded [here](https://code.visualstudio.com/).

2. Begin by cloning this repository: `git clone https://github.com/intersystems/multi-model-exercise`.

2. Open the connections.config file in the top-level directory. Enter the InterSystems IP and Port listed for your InterSystems IRIS instance and click Save. If you are using the [InterSystems IRIS sandbox instance](https://www.intersystems.com/try-intersystems-iris-for-free/), you only need to update the IP field to match the ‘external ip’ field found in your lab. If you are using the InterSystems [InterSystems IRIS community edition through Docker](https://hub.docker.com/_/intersystems-iris-data-platform), you will need to follow a few extra steps:
	  * Install Docker 
	  * Run `docker run --name my-iris2 -d -p 52773:52773 -p 51773:51773 store/intersystems/iris-community:2020.1.0.215.0` 
	  * Navigate to `http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen` and update your password. If necessary, replace 'localhost' with your computer's IP address
	  * Change your password in the connections.config file to the one you chose. Change the port value to `51773` and change the IP to 'localhost' or your computer's IP address.


## Create The Table Schema Using Python
1. Install and configure Python
  	* Run `cd ./python`
	* On the sandbox:
		* Run `odbcinst -i -d -f pyodbc_wheel/linux/odbcinst.ini`
	* On macOS:
		* Install [homebrew](https://brew.sh/)
		* Run `brew install unixodbc`
		* Run `odbcinst -i -d -f pyodbc_wheel/mac/odbcinst.ini`
		* Run `pip install pip==7.1.2`
		* Run `pip install --upgrade --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" --allow-external pyodbc --allow-unverified pyodbc pyodbc`
	* On Windows:
		* Run `./pyodbc_wheel/ODBC-2019.1.0.510.0-win_x64.exe`
		* Run `pip install pyodbc`
			* If the `pip` command is not recognized, you can also use `py -m pip install` for any `pip` installation command.
		
		
2. In the IDE provided with your sandbox or Visual Studio Code, open `python/createSchema.py` and scroll down to the `create_employee` function. Below the function declaration, uncomment the following code:

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
	
	**Note**: if you are using python 2 or earlier, follow the commented instructions in `createschema.py` in the `connect_to_iris()` function to configure the connection properly.

3. Run `python createSchema.py`. If successful, the terminal will output `Created table Demo.Employee successfully`.
   * **Note**: This exercise is configured for Python 3. For some users, you may need to run `python3 createSchema.py` if the `python` command defaults to Python 2. 
	
4. Confirm that the `Demo.Employee` table has been created.
   1. Open the Management Portal by following the link provided when you created your instance of the InterSystems IRIS sandbox. If you are using the Docker container, go to [http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen](http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen). 
   3. Navigate to **System Explorer > SQL** and expand the **Tables** section. Find `Demo.Employee` in the list.


## Modify the table class using InterSystems ObjectScript

### Setting Up the Visual Studio Code ObjectScript Extension

1. [Install InterSystems Visual Studio Code](https://code.visualstudio.com/), if you have not already done so.
2. Open Visual Studio code. In the Extensions Manager, search for and install the `InterSystems ObjectScript` extension.
3. Select a folder for your workspace by selecting **Open Folder** in the File Explorer, or **File** > **Open**. Select or create a folder on your local machine to store settings specific to your workspace.
3. Open your Visual Studio Code settings (**File** (or **Code** if on macOS) > **Preferences** > **Settings** > **InterSystems ObjectScript** and select **Edit in settings.json**. Paste the following JSON, filling in the settings for your InterSystems IRIS instance connection:
	```javascript
	{
		"objectscript.conn": {
			"active": true, 
			"label": "LOCAL",
			"host": "<ip for your instance>", // If using Sandbox, use the Atelier Server Address provided.
			"port": 80, // If using Sandbox, the Atelier Server Port provided.
			"username": "tech",
			"password": "demo",
			"ns": "USER", // this is the namespace you wish to connect to 
			"https": false
		}
	}
	```

2. Navigate to the ObjectScript extension in your Visual Studio Code, right click `Classes/Demo/Employee.cls` and select **Export**.

8. Navigate to the **File Explorer** and open the newly created `src/Demo/Employee.cls` file.


### Modifying Classes With Visual Studio Code


1. At the top of the Demo.Employee class, change `Extends %Persistent` to `Extends (%Persistent, %JSON.Adaptor)`.

InterSystems ObjectScript is an object-oriented programming language that supports multiple inheritance.  This means that by inheriting the `%JSON.Adaptor` class, your table is now automatically able to import JSON data into instances. For more information on the `%JSON.Adaptor` class read [Using the JSON Adaptor](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GJSON_adaptor).

11.  Because our table includes an auto-incremented primary key, we need to tell the `JSON.Adaptor` class not to look for that field in incoming JSON files, but to output it as a field when exporting class instances to JSON format.  To do this, find the ID property in the Employee class and add `(%JSONINCLUDE = "outputonly")` after `%Library.AutoIncrement`.

12. Before we can run this file, we need to add one small class method to expose the functionality of the `%JSON.Adaptor` class to the Native API (and, by extension, to our Node.js application).  Below the Property and Parameter declarations in the `Demo.Employee` class, paste the following code.

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
13. Make sure to recompile the `Demo.Employee` class by saving it. You have now configured your SQL table class to receive JSON data and automatically create a new record from it. 

Note: The completed ObjectScript `Employee` class is included in this repository for your reference at `ObjectScript/Demo.Employee.cls`.

## Create A Node.js App to send JSON files to your database.
1. If you do not have Node.js installed locally, download and install it [here](https://nodejs.org/en/download/). If you are using the InterSystems IRIS sandbox, you can skip this step.
	* **Note**: once Node.js is installed, you may need to restart your terminal in order for it to recognize `node` commands.

12. Run `cd ../nodeApp`

12. Create a new file called `record.json` containing the following JSON oject:

	```javascript
	{
		"Name": "JJ Smith",
		"Title": "Software Engineer",
		"Department": "Engineering"
	}
	```

13. Run `npm install --save intersystems-iris-native`. This installs the InterSystems IRIS Native API, which enables you to both access the underlying data structures in your database, and to call ObjectScript class methods directly from your code.


12. Open the `app.js` file. Navigate to `const Iris = connection.createIris()` and uncomment the following lines:

	```JavaScript
	let record = JSON.parse(fs.readFileSync("./record.json", "utf8"))
	Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(record))
	console.log(`Created new record in Demo.Employee table.`)
	```

	This code calls a class method using the Native API and passes a JSON string as a parameter. For more information, see [Calling ObjectScript Methods and Functions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=BJSNAT_call)

12. In the terminal, type `node app.js`. The node application will output that it has created a new record.



## Query The Database With Python
1.  `cd` back into the Python directory (`cd ../python`)

2.  Run `python query.py`. You should see the results of the SQL query, which includes the record of JJ Smith that you inserted using Node.js.

## Troubleshooting

Problem | Likely Solution 
------------------------- | ------------------------
I get a 'Data source name not found' error when I run `python createSchema.py`| You may have the 32-bit version of Python installed on your computer instead of the 64-bit.
My node.js app quits unexpectedly when I click **Submit**. | Make sure that you click **Save** in Visual Studio Code and that the class compiled successfully. 
I'm on a Windows and the `python` command is not recognized. 	| Be sure to add python to your environment variables. 

## Further Resources

* Visit [GettingStarted.InterSystems.com](https://gettingstarted.intersystems.com) to learn more about InterSystems IRIS data platform.

* The [Multi-Model QuickStart](https://gettingstarted.intersystems.com/multimodel-overview/multimodel-quickstart/) provides a quick introduction to how to use the multi-model capabilities of InterSystems IRIS in the language of your choosing.

* Try the (Globals QuickStart)[https://gettingstarted.intersystems.com/multimodel-overview/globals-quickstart/] to learn about the proprietary data structure that comes with InterSystems IRIS data platform.
