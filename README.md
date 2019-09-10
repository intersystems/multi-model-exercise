Multi-Model Exercise

Installation steps:

git clone https://github.com/zkrowiak/multi-model-exercies

1.	Open connections.config

2.	Enter the Intersystems IP and Port listed for your intersystem IRIS instance and save.

3.	Install and configure python
  * cd int multi-model-exercises/python
  * If in IDE on windows, run `pip install pyodbc`
  * run `odbcinst -i -d -f pyodbc_wheel/odbcinst.ini`
	
4.	Edit the connections.config file to replace the IP and Port values with those supplied by your intersystem instance.

5.	Run `python createSchema.py`
  *This creates the the SQL table in InterSystems IRIS
	
6.	Open the management portal and navigate to System Explorer/SQL and expand the ‘Tables’ section.  
  * Observe that the Demo.Employee table has been created.

7.	Open Atelier and connect your IRIS instance to it. 

8.	Create a new project connected to this server

9.	In the Atelier server explorer, right click the Demo.Employee class and click ‘Copy to Project” and select the project you just created.

10.	Back in the Atelier explorer, navigate into the Demo package, right click “Demo” and select ‘new’ and then, Atelier Class.  Call the class Demo.JSONMaker
  * Copy and paste the code from the class of that name in your Github repo 
  * Compile that class
  *  Go to the Demo.Employee class and at the top where it says `extends %Persistant` change it to `Extends (%Persistent, 		JSONMaker)`
  * Find the ID property in the Employee class and add `(%JSONINCLUDE = "outputonly")` after `%Library.AutoIncrement`
  * You have now configured your SQL table class to receive JSON data and automatically create a new record from it.

11.	Install and configure Node.js
  * TODO (NEED UPDATED TRY INSTANCE)

12.	In the terminal, type node app.js

13.	Navigate to the ip address outputted to the terminal.
  * You should see a simple HTML form with inputs for all of the fields in your Demo.Employee table.
  * Enter John Smith, Software Engineer, Engineering for the three fields and click submit

14.	CD back into the Python directory

15.	Run python query.py
  * You should see outputted the results of the SQL query, which includes the record you inserted through Node of John 			Smith.
