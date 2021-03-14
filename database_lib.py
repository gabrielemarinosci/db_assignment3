import mysql.connector
import csv

def create_db (cursor, DB_NAME):

    try:
        cursor.execute(f'CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET "utf8"')
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def get_data (file_path):
    
    rows = []

    with open(file_path) as f:
        
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            rows.append(tuple(row))

    return rows;
  

def create_table(cursor, table_name, csv_path, queries):

    data = get_data(csv_path)
    cursor.execute(queries[0])
    cursor.executemany(queries[1], data)

def initialization(cursor):

    companies_table = ('''CREATE TABLE companies 
                        (name VARCHAR(50) PRIMARY KEY,
                        ceo VARCHAR(50),
                        foundation INT,
                        total_employees INT)''',
                       '''INSERT INTO companies
                          VALUES (%s, %s, %s, %s)''')

    games_table = ('''CREATE TABLE games
                      (title VARCHAR(50) PRIMARY KEY,
                      genre VARCHAR(50),
                      release_date INT,
                      company VARCHAR(50),
                      publisher VARCHAR(50))''',
                  '''INSERT INTO games
                      VALUES (%s, %s, %s, %s, %s)''')
    
    dep_table = ('''CREATE TABLE departments
                    (name VARCHAR(50),
                    company VARCHAR(50),
                    n_employees INT,
                    head_department VARCHAR(50),
                    PRIMARY KEY (name, company))''',
                '''INSERT INTO departments
                    VALUES (%s, %s, %s, %s)''')

    employee_table = ('''CREATE TABLE employees 
                         (name VARCHAR(50),
                         age INT,
                         company VARCHAR(50),
                         employeeID VARCHAR(10),
                         department VARCHAR(50),
                         address VARCHAR(50),
                         PRIMARY KEY (employeeID, name))''',
                      '''INSERT INTO employees
                        VALUES (%s, %s, %s, %s, %s, %s)''')

    path = '/Users/gabrielemarinosci/Desktop/Database/ass2/companies - Foglio1.csv'
    create_table(cursor, 'companies', path, companies_table)
    path = '/Users/gabrielemarinosci/Desktop/Database/ass2/games - Foglio1.csv'
    create_table(cursor, 'games', path, games_table)
    path = '/Users/gabrielemarinosci/Desktop/Database/ass2/departments - Foglio1.csv'
    create_table(cursor, 'departments', path, dep_table)
    path = '/Users/gabrielemarinosci/Desktop/Database/ass2/employees - Foglio1.csv'
    create_table(cursor, 'employees', path, employee_table)