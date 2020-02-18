# Multi-Model Exercise

This exercise takes you through the steps to use InterSystems IRIS multi-model capability to create a Node.js application that  sends JSON data straight to your database instance without any parsing or mapping. If you have not already, we recommend also looking at the [Multi-Model Quickstart](https://gettingstarted.intersystems.com/multimodel-overview/multimodel-quickstart/). We will use Python, JavaScript, and InterSystems ObjectScript to interact with the data from different contexts. First, we will use Python to create our table schema using standard SQL statements.  Then, we will modify the underlying ObjectScript class for that table to allow it to receive and persist JSON data directly. Next, we will create a simple Node.js application that will send JSON files to our instance of InterSystems IRIS. Finally, we will query that database using Python again to see how the same data could be accessed in multiple languages from multiple contexts.

## Installation steps:

1. This exercise requires the 64-bit version of Python 3.
	* If you already have Python installed, make sure to check what bit version you are using by launching the python shell by typing `python` .  If the version is 2, try quitting the shell (`control-z + enter` on Windows, `control-d` on Mac) and typing `python3` .
	* Install Python by going here https://www.python.org/downloads/ (be sure to check off 'Add Python to environment variables' in the'Advanced Options' section of the installation.

	* NOTE: do not click the 'Download Python 3.7.4' button directly on that site as it might download the 32 bit version of python, which will not work with the exercise. Make sure to select the link to your operating system and download the 64 bit Python file.
	* You may need to restart your terminal or even add python to the PATH environment variable if the python command does not work after installing python.

2. Begin by downloading this repository to your local machine `git clone https://github.com/intersystems/multi-model-exercise`.

2. Open the connections.config file in the top-level directory.

3. Enter the Intersystems IP and Port listed for your intersystem IRIS instance and save. If you are using the InterSystems IRIS Learning Labs instance (which can be found [here](https://www.intersystems.com/try-intersystems-iris-for-free/)), enter the IP and Port listed under 'External Connections.' If you are using the InterSystems [InterSystems IRIS community edition through Docker](https://hub.docker.com/_/intersystems-iris-data-platform), you will need to follow a few extra steps:
	  * Install Docker 
	  * Run `docker run --name my-iris2 -d -p 52773:52773 -p 51773:51773 store/intersystems/iris-community:2019.3.0.302.0` 
	  * Navigate to `http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen` and update your password. If necessary, replace 'localhost' with your computer's IP address
	  * Change your password in the connections.config file to the one you chose. Change the port value to `51773` and change the IP to 'localhost' or your computer's IP address.


## Create The Table Schema Using Python
1. Install and configure python
  	* Run `cd ./python`
	* If on a Mac:
		* Install [homebrew](https://brew.sh/)
		* Run `brew install unixodbc`
		* Run `odbcinst -i -d -f pyodbc_wheel/odbcinst.ini`
		* Run `pip install pip==7.1.2`
		* Run `pip install --upgrade --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" --allow-external pyodbc --allow-unverified pyodbc pyodbc`
	* If on a Windows:
		* Run `./pyodbc_wheel/ODBC-2019.1.0.510.0-win_x64.exe`
		* Run `pip install pyodbc`
			* If the `pip` command is not recognized, you can also use `py -m pip install` for any `pip` installation command.
		
		

2. In your preferred IDE or text editor, open `python/createSchema.py` and scroll down to the `create_employee` function. Below the function declaration, insert the following code:

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
	
	Note: if you are using python 2 or earlier, follow the commented instructions in `createschema.py` in the `connect_to_iris()` function to configure the connection properly.

3. Run `python createSchema.py`. 
	* Note: This exercise is configured for Python 3. For some users, you may need to run `python3 createSchema.py` if the `python` command defaults to Python 2. 
	
1. Open the management portal by following the link given to you when you created your instance of the InterSystems IRIS learning labs (or if on the docker container, go to [http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen](http://localhost:52773/csp/sys/%25CSP.Portal.Home.zen), navigate to **System Explorer > SQL** and expand the **Tables** section.  Observe that the Demo.Employee table has been created.
## Modify the table class using InterSystems ObjectScript

### Setting Up Atelier

1. If you have not installed InterSystems Atelier, follow [these instructions](https://download.intersystems.com/download/atelier.csp). Once downloaded and installed, open Atelier and connect your InterSystems IRIS instance to it.  

	Atelier allows you to edit InterSystems IRIS classes directly so that you can customize how they behave. When you ran `createSchema.py` earlier, InterSystems IRIS automatically created an ObjectScript class that represents that table.  We will need to modify this class to enable it to receive JSON data.

2. In the Atelier perspective, navigate to the **Server Explorer** and select the green 'plus' sign to create a new server. Give it a name, and supply it with the IP, Port, and login info you used in your connections.config file.

8. Switch to the **Atelier Explorer** and create a project in Atelier to store a local copy of your Demo.Employee class so that you can edit it.

9. Next, back in the **Server Explorer** right click the `Demo.Employee` class, click ‘Copy to Project” and select the project you just created.

### Modifying Classes With Atelier


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

## Create A Node.js App to send JSON files to your database.
1. If you do not have Node.js installed locally, download and install it [here](https://nodejs.org/en/download/).
	* Note: once Node.js is installed, you may need to restart your terminal in order for it to recognize `node` commands.

12. Run `cd ../nodeApp`

12. Run `npm install ip`

13. Run `npm install --save intersystems-iris-native`. This installs the InterSystems IRIS Native API, which enables you to both access the underlying data structures in your database, and to call ObjectScript class methods directly from your code.

12. Open the `app.js` file and navigate down to the line `body = querystring.parse(body)` and paste the following lines below that .

	```JavaScript
		  //call the classmethod in the Employee class to create and persists a new database record
		  Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(body))
	```

	This code calls a class method using the Native API and passes a JSON string as a parameter.  For more information, 		see [Calling ObjectScript Methods and Functions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=BJSNAT_call)

12. In the terminal, type `node app.js`

13. Navigate to the IP address outputted to the terminal. You should see a simple HTML form with inputs for all of the fields in your Demo.Employee table.

14. Enter `JJ Smith`, `Software Engineer`, and `Engineering` for the three fields and click submit.

## Query The Database With Python
14. Quit the Node.js server by pressing `control-c` and `cd` back into the Python directory (`cd ../python`)

15. Run `python query.py` You should see outputted the results of the SQL query, which includes the record you inserted through Node of JJ Smith.


# Troubleshooting

Problem | Likely Solution 
------------------------- | ------------------------
When I run python createSchema.py I get a 'Data source name not found' error | You may have the 32 bit version of python installed on your computer instead of the 64 bit.
When I run createSchema.py I get an error about consistant tabs or spaces | When pasting the create_table statement, make sure that the variable name (`create_table`) is declared at the same indentation level as the preceding declarations. 
My node.js app quits unexpectedly when I hit 'submit' | Make sure you hit save in Atelier and that the class compiled successfully. 
I'm on a Windows and the `python` command is not recognized. 	| Be sure to add python to your environment variables. 

