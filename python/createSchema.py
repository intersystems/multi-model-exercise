import pyodbc



def connect_to_iris():
    # Login credentials
    driver = "{InterSystems ODBC}"
    ip = "172.24.2.254"
    port = 51773
    namespace = "USER"
    username = "SuperUser"
    password = "SYS"

    # Connect to InterSystems IRIS using PyODBC
    connection_string = 'DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'\
        .format(driver, ip, port, namespace, username, password)
    pyodbc_connection = pyodbc.connect(connection_string)

    print("Connected to InterSystem IRIS")
    return pyodbc_connection


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
    except:
        delete_old_table(cursor, "Demo.Employee")
        cursor.execute(create_employee)

    connection.commit()

def run():
    # Get connections for PyODBC
    pyodbc_connection = connect_to_iris()

    # Populate and retrieve data using PyODBC
    create_employee(pyodbc_connection)



if __name__ == '__main__':
    run()