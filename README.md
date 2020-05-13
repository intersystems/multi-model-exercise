# Multi-Model Exercise

This exercise takes you through the steps to use InterSystems IRIS multi-model capability to create a Node.js application that  sends JSON data straight to your database instance without any parsing or mapping. We will use Python, JavaScript, and InterSystems ObjectScript to interact with the data from different contexts. First, we will use Python to create our table schema using standard SQL statements.  Then, we will modify the underlying ObjectScript class for that table to allow it to receive and persist JSON data directly. Next, we will create a simple Node.js application that will send JSON files to our instance of InterSystems IRIS. Finally, we will query that database using Python again to see how the same data could be accessed in multiple languages from multiple contexts.

## Installation steps:
We recommend using the [InterSystems IRIS Sandbox](www.intersystems.com/try) to run this exercise, in which case you can skip the following installation steps for running it on your local machine.  
1. This exercise requires the 64-bit version of Python 3.
	* If you already have Python installed, make sure to check what bit version you are using by launching the python shell by typing `python` .  If the version is 2, try quitting the shell (`control-z + enter` on Windows, `control-d` on macOS) and typing `python3` .
	* Install Python by going here https://www.python.org/downloads/ (be sure to check off 'Add Python to environment variables' in the 'Advanced Options' section of the installation.

	* **Note**: do not click the 'Download Python 3.7.4' button directly on that site as it might download the 32 bit version of python, which will not work with the exercise. Make sure to select the link to your operating system and download the 64 bit Python file.
	* You may need to restart your terminal or even add python to the PATH environment variable if the python command does not work after installing python.

2. Begin by downloading this repository to your local machine `git clone https://github.com/intersystems/multi-model-exercise`.

2. Open the connections.config file in the top-level directory.

3. Enter the InterSystems IP and Port listed for your InterSystems IRIS instance and save. If you are using the InterSystems IRIS Sandbox instance (which can be found [here](https://www.intersystems.com/try-intersystems-iris-for-free/)), you only need to update the ip field to match the ‘external ip’ field found in your lab. If you are using the InterSystems [InterSystems IRIS community edition through Docker](https://hub.docker.com/_/intersystems-iris-data-platform), you will need to follow a few extra steps:
	  * Install Docker 
	  * Run `docker run --name my-iris2 -d -p 52773:52773 -p 51773:51773 store/intersystems/iris-community:2020.1.0.215.0` 
	  * Navigate to `http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen` and update your password. If necessary, replace 'localhost' with your computer's IP address
	  * Change your password in the connections.config file to the one you chose. Change the port value to `51773` and change the IP to 'localhost' or your computer's IP address.


## Create The Table Schema Using Python
1. Install and configure python
  	* Run `cd ./python`
	* If on the sandbox:
		* Run `odbcinst -i -d -f pyodbc_wheel/linux/odbcinst.ini`
	* If on macOS:
		* Install [homebrew](https://brew.sh/)
		* Run `brew install unixodbc`
		* Run `odbcinst -i -d -f pyodbc_wheel/mac/odbcinst.ini`
		* Run `pip install pip==7.1.2`
		* Run `pip install --upgrade --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" --allow-external pyodbc --allow-unverified pyodbc pyodbc`
	* If on Windows:
		* Run `./pyodbc_wheel/ODBC-2019.1.0.510.0-win_x64.exe`
		* Run `pip install pyodbc`
			* If the `pip` command is not recognized, you can also use `py -m pip install` for any `pip` installation command.
		
		
2. In the IDE provided with your Sandbox or Visual Studio Code, open `python/createSchema.py` and scroll down to the `create_employee` function. Below the function declaration, insert the following code:

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

3. Run `python createSchema.py`. 
   * **Note**: This exercise is configured for Python 3. For some users, you may need to run `python3 createSchema.py` if the `python` command defaults to Python 2. 
	
4. Validate the `Demo.Employee` table has been created.
   1. Open the management portal by following the link given to you when you created your instance of the InterSystems IRIS sandbox (or if on the docker container, go to [http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen](http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen). 
   2. Switch to the `USER` namespace, if necessary, by clicking "Switch" next to "Namespace %SYS"
   3. Navigate to **System Explorer > SQL** and expand the **Tables** section. Find `Demo.Employee` in the list.


## Modify the table class using InterSystems ObjectScript

### Setting Up the Visual Studio Code ObjectScript Extension

1. If you have not installed InterSystems Visual Studio Code, do so  [here](https://code.visualstudio.com/).
2. Open Visual Studio code. In the extensions manager, search for and install the `InterSystems ObjectScript` extension.
3. Select a folder for your workspace by selecting **Open Folder** in the **File Explorer**, or **File** > **Open**. Navigate to the folder where you .
3. Open your Visual Studio Code settings (**File** (or **Code** if on macOS) > **Preferences** > **Settings** > **InterSystems ObjectScript** and select **Edit in settings.json**.  Paste the following JSON, filling in the settings for your InterSystems IRIS instance connection:
	```javascript
	"objectscript.conn": {
		"active": true, 
		"label": "LOCAL",
		"host": "<ip for your instance>", // If using Sandbox, use the Atelier Server Address provided.
		"port": 80, // If using Sandbox,  the Atelier Server Port provided.
		"username": "tech",
		"password": "demo",
		"ns": "USER", // this is the namespace you wish to connect to 
		"https": false
	}
	```

2. Navigate to  on the ObjectScript extension in your Visual Studio Code, right click `Demo/Employee.cls` and select **Export**.

8. Navigate to the **File Explorer** and open the newly created `src/Demo/Employee.cls` file.

9. Next, back in the **Server Explorer** right click the `Demo.Employee` class, click ‘Copy to Project” and select the project you just created.

### Modifying Classes With Visual Studio Code


1. In the Demo.Employee class and at the top where it says `Extends %Persistent` change it to `Extends (%Persistent, 		%JSON.Adaptor)`.  InterSystems ObjectScript is an object-oriented programming language that supports multiple-inheritance.  This means that by inheriting the `%JSON.Adaptor` class, your table is now automatically able to import JSON data into instances.  For more information on the `%JSON.Adaptor` class [look here](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GJSON_adaptor).

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
13. Make sure to recompile the Demo.Employee class by saving it. You have now configured your SQL table class to receive JSON data and automatically create a new record from it. 

Note: The completed ObjectScript `Employee` class is included in this repository for your reference at `ObjectScript/Solution.Employee.cls`.

## Create A Node.js App to send JSON files to your database.
1. If you do not have Node.js installed locally, download and install it [here](https://nodejs.org/en/download/). If you are using the InterSystems IRIS Sandbox, you can skip this step.
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


12. Open the `app.js` file and navigate down to the line `const Iris = connection.createIris()` and paste the following lines below that.

	```JavaScript
	let record = JSON.parse(fs.readFileSync("./record.json", "utf8"))
	Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(record))
	console.log(`Created new record`)
	```

	This code calls a class method using the Native API and passes a JSON string as a parameter.  For more information, see [Calling ObjectScript Methods and Functions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=BJSNAT_call)

12. In the terminal, type `node app.js`. The node application will output that it has created a new record.



## Query The Database With Python
1.  `cd` back into the Python directory (`cd ../python`)

2.  Run `python query.py` You should see outputted the results of the SQL query, which includes the record you inserted through Node of JJ Smith.

## Troubleshooting

Problem | Likely Solution 
------------------------- | ------------------------
When I run `python createSchema.py` I get a 'Data source name not found' error | You may have the 32 bit version of python installed on your computer instead of the 64 bit.
When I run `python createSchema.py` I get an error about inconsistent tabs or spaces | When pasting the create_table statement, make sure that the variable name (`create_table`) is declared at the same indentation level as the preceding declarations. 
My node.js app quits unexpectedly when I hit 'submit' | Make sure you hit save in Visual Studio Code and that the class compiled successfully. 
I'm on a Windows and the `python` command is not recognized. 	| Be sure to add python to your environment variables. 

## Further Resources

* Visit [GettingStarted.InterSystems.com](https://gettingstarted.intersystems.com) to learn more about the InterSystems IRIS data platform.

* The [Multi-Model QuickStart](https://gettingstarted.intersystems.com/multimodel-overview/multimodel-quickstart/) provides a quick introduction to how to use the multi-model capabilities of InterSystems IRIS in the language of your choosing.

* Try the [Globals QuickStart][https://gettingstarted.intersystems.com/multimodel-overview/globals-quickstart/] to learn about the proprietary data structure that comes with the InterSystems IRIS data platform.
