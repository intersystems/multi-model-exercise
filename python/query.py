import pyodbc
import createSchema

def main():
    connection, _ = createSchema.connect_to_iris()

    queryStr = '''
        SELECT * FROM Demo.Employee
    '''

    cursor = connection.cursor()
    for row in cursor.execute(queryStr):
        print(row)


if __name__ == "__main__":
    main()