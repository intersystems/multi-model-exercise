import pyodbc
import createSchema

def main():
    connection = createSchema.connect_to_iris()
    queryStr = '''
        SELECT * FROM Demo.Employee
    '''

    cursor = connection.cursor()
    cursor.execute(queryStr)
    for row in cursor:
        print("{}".format(row))


if __name__ == "__main__":
    main()