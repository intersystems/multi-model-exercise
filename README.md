# Multi-Model Exercise

This exercise takes you through the steps to use InterSystems IRIS multi-model capability to create a Node.js application that to sends JSON data straight to the database without any parsing or mapping. We will use Python, JavaScript, and InterSystems ObjectScript to interact with the data from different contexts. First, we will use Python to create our table schema using standard SQL statements.  Then, we will modify the underlying ObjectScript class for that table to allow it to receive and persist JSON data directly. Next, we will create a simple Node.js application that will send JSON files to our instance of InterSystems IRIS. Finally, we will query that database using Python again to see how the same data could be accessed in multiple languages from multiple contexts.

## Installation steps:

1. Begin by downloading this repository to your local machine `git clone https://github.com/zkrowiak/multi-model-exercies`

2. Open the connections.config file in the top-level directory

3. Enter the Intersystems IP and Port listed for your intersystem IRIS instance and save


## Create The Table Schema Using Python
1. Install and configure python
  	* Follow [these directions to install pydobc](https://github.com/intersystems/quickstarts-python/blob/master/pyodbc_install.md)
  	* cd into `multi-model-exercises/python`

2. In your preferred IDE, open `python/createSchema.py` and scroll down to the `create_employee` function. Below the function declaration, insert the following code:

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

3. Run `python createSchema.py`. 

## Modify the table class using InterSystems ObjectScript
	
1. Open the management portal by following the link given to you when you created your instance of the InterSystems IRIS learning labs, navigate to **System Explorer > SQL** and expand the **Tables** section.  Observe that the Demo.Employee table has been created.

7.If you have not installed InterSystems Atelier, follow [these instructions](https://download.intersystems.com/download/atelier.csp). Once downloaded and installed, open Atelier and connect your IRIS instance to it.  

Atelier allows you to edit InterSystems IRIS classes directly so that you can customize how they behave. When you ran `createSchema.py` earlier, IRIS automatically created an ObjectScript class that represents that table.  We will need to modify this class to enable it to receive JSON data.

8. Begin by creating a project in Atelier to store a local copy of your Demo.Employee class so that you can edit it.

9. In the Atelier server explorer, right click the `Demo.Employee` class, click ‘Copy to Project” and select the project you just created.

10. In the Demo.Employee class and at the top where it says `Extends %Persistant` change it to `Extends (%Persistent, 		%JSON.Adaptor)`.  InterSystems ObjectScript is an object-oriented programming language that supports multiple-inheritance.  This means that by inheriting the `%JSON.Adaptor` class, your table is now automatically able to import JSON data into instances.  For more information on the `%JSON.Adaptor` class [look here](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GJSON_adaptor)

11.  Because our table includes an auto_incremented primary key, we need to tell the `JSON.Adaptor` class not to look for that field in incoming JSON files, but to output it as a field when exporting class instances to JSON format.  To do this, find the ID property in the Employee class and add `(%JSONINCLUDE = "outputonly")` after `%Library.AutoIncrement`.

12. Before we can run this file, we need to add one small function to expose the functionality of the `%JSON.Adaptor` class to the Native API (and, by extension, to our Node.js application).  Below the Property and Parameter declarations in the `Demo.Employee` class, paste the following code.

```ObjectScript
ClassMethod fromJSON(j as %String) As %Integer

{
	set e = ..%New() 	//create a new class instance
	do e.%JSONImport(j) 	//call the %JSON.Adapter instance method to import JSON string
 	set e.ID = 0 		//this field must be set to 0 for the %Library.AutoIncrement class to increment correctly
 	
	do e.%Save() 		//this persists the instance
	
	
	
	
	return 1
}
```
13. Make sure to recompile the Demo.Employee class by saving it. You have now configured your SQL table class to receive JSON data and automatically create a new record from it.

## Create A Node.js App to send JSON files to your database.
11. If you do not have Node.js installed locally, download and install it [here](https://nodejs.org/en/download/)

12. `cd` into the nodeApp directory

13. Run `npm install --save intersystems-iris-native`. This installs the InterSystems IRIS Native API, which enables you to both access the underlying data structures in your database, and to call ObjectScript class methods directly from your code.

12. Open the `app.js` file and navigate down to the line `body = querystring.parse(body)` and paste the following lines below that 

	```JavaScript
		  //call the classmethod in the Employee class (inherited from the JSONMaker superclass)
		  Iris.classMethodValue("Demo.Employee", "fromJSON", JSON.stringify(body))
	```

	This code calls a class method using the Native API and passes a JSON string as a parameter.  For more information, 		see [Calling ObjectScript Methods and Functions](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=BJSNAT_call)

12. In the terminal, type node app.js

13.	Navigate to the ip address outputted to the terminal.
  * You should see a simple HTML form with inputs for all of the fields in your Demo.Employee table.
  * Enter John Smith, Software Engineer, Engineering for the three fields and click submit

14.	Quit the Node.js server by pressing control-c and CD back into the Python directory

15.	Run python query.py
  * You should see outputted the results of the SQL query, which includes the record you inserted through Node of John 			Smith.
