import pyodbc
import os



def connect_to_iris():
    # Login credentials

    connection = get_connection_config()
    # Connect to InterSystems IRIS using PyODBC
    connection_string = 'DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'\
        .format(connection['driver'], connection['ip'], int(connection['port']),\
         connection['namespace'], connection['username'], connection['password'])
    pyodbc_connection = pyodbc.connect(connection_string)

    print("Connected to InterSystem IRIS")
    return pyodbc_connection

def get_connection_config():
    with open("../connections.config") as f:
        f = f.read()
        f = f.split("\n")
        dict = {}
        for line in f:
            line = line.split(":")
            dict[line[0].strip()] = line[1].strip()
        return dict

# Remove old table if exist
def delete_old_table(cursor, table_name):
    drop_table = "DROP TABLE {}".format(table_name)
    cursor.execute(drop_table)


def create_employee(connection):
    # Create cursor
    cursor = connection.cursor()

    # Create Demo.Location table in the InterSystems IRIS database
    create_employee = """
        CREATE TABLE Demo.Employee(
            ID Integer PRIMARY KEY AUTO_INCREMENT,
            Name varchar(256),
            Title varchar(256), 
            Department varchar(50)
        )
    """
    try:
        cursor.execute(create_employee)
    except Exception as e:
        print("need to delete old table",e)
        delete_old_table(cursor, "Demo.Employee")
        cursor.execute(create_employee)

    connection.commit()
    print("created table successfully")

def run():
    # Get connections for PyODBC
    pyodbc_connection = connect_to_iris()

    # Populate and retrieve data using PyODBC
    create_employee(pyodbc_connection)



if __name__ == '__main__':
    run()