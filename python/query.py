import pyodbc
import irisnative


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

    # Connect to InterSystems IRIS using the Native API
    nativeapi_connection = irisnative.createConnection(ip, port, namespace, username, password)

    print("Connected to InterSystem IRIS")
    return pyodbc_connection, nativeapi_connection


# Remove old table if exist
def delete_old_table(cursor, table_name):
    drop_table = "DROP TABLE {}".format(table_name)
    cursor.execute(drop_table)


def populate_airports(connection):
    # Create cursor
    cursor = connection.cursor()

    # Create Demo.Location table in the InterSystems IRIS database
    create_employees = """
        CREATE TABLE Demo.Employee(
            ID Integer PRIMARY KEY,
            Name varchar(256),
            Title varchar(256), 
            Department varchar(50)
        )
    """
    try:
        cursor.execute(create_employees)
    except:
        delete_old_table(cursor, "Demo.Location")
        cursor.execute(create_employees)

    # Create Demo.Airport table in the InterSystems IRIS database


    #  Insert locations into Demo.Location table in the InterSystems IRIS database
    # insert_locations = """
    #     Insert into Demo.Location
    #     (zip, city, state)
    #     VALUES (?, ?, ?)
    # """
    # for zip, city, state in LOCATIONS:
    #     cursor.execute(insert_locations, zip.encode('utf-8'), city.encode('utf-8'), state.encode('utf-8'))

    # # Insert airport into Demo.Airport table in the InterSystems IRIS database
    # insert_airports = """
    #     Insert into Demo.Airport
    #     Select ?, ?, Demo.Location.id
    #     FROM Demo.Location 
    #     where Demo.Location.zip = ?
    # """
    # for name, code, zip in AIRPORTS:
    #     cursor.execute(insert_airports, name.encode('utf-8'), code.encode('utf-8'), zip.encode('utf-8'))

    connection.commit()

def run():
    # Get connections for PyODBC and the Native API
    pyodbc_connection, nativeapi_connection = connect_to_iris()

    # Populate and retrieve data using PyODBC
    populate_airports(pyodbc_connection)
    # get_airports(pyodbc_connection)

    # Create an IRIS native object
    # iris_native = irisnative.createIris(nativeapi_connection)

    # Uncomment the following lines to store and retrieve data natively using the Native API
    # store_airfare(iris_native)
    # check_airfare(iris_native)


if __name__ == '__main__':
    run()