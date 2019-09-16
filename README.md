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

10. In the Demo.Employee class and at the top where it says `extends %Persistant` change it to `Extends (%Persistent, 		JSONMaker)`
  * Find the ID property in the Employee class and add `(%JSONINCLUDE = "outputonly")` after `%Library.AutoIncrement`
  * Make sure to recompile the Demo.Employee class by saving it.
  * You have now configured your SQL table class to receive JSON data and automatically create a new record from it.

11.	Install and configure Node.js
  * `cd` into the nodeApp directory
  * run `npm install --save intersystems-iris-native`

12.	In the terminal, type node app.js

13.	Navigate to the ip address outputted to the terminal.
  * You should see a simple HTML form with inputs for all of the fields in your Demo.Employee table.
  * Enter John Smith, Software Engineer, Engineering for the three fields and click submit

14.	Quit the Node.js server by pressing control-c and CD back into the Python directory

15.	Run python query.py
  * You should see outputted the results of the SQL query, which includes the record you inserted through Node of John 			Smith.
