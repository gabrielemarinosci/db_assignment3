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
            
    path = r"C:\Users\foxra\Desktop\Courses\Database\db_assignment3\companies - Foglio1.csv"
    create_table(cursor, 'companies', path, companies_table)
    path = r"C:\Users\foxra\Desktop\Courses\Database\db_assignment3\games - Foglio1.csv"
    create_table(cursor, 'games', path, games_table)
    path = r"C:\Users\foxra\Desktop\Courses\Database\db_assignment3\departments - Foglio1.csv"
    create_table(cursor, 'departments', path, dep_table)
    path = r"C:\Users\foxra\Desktop\Courses\Database\db_assignment3\employees - Foglio1.csv"
    create_table(cursor, 'employees', path, employee_table)

def company_ceo(cursor):
    company = input("Enter the name of the company: ")
    query = (f"SELECT ceo FROM companies WHERE name = '{company}'") 
    cursor.execute(query)
    for i in cursor:
        print(i[0])

def age_difference_between_different_departments(cursor):
    department_one = input("Enter the name of the first department(Programming, Graphic-design, Management) ")
    department_two = input("Enter the name of the second department(Programming, Graphic-design, Management) ")
    query1 = (f"SELECT AVG(age) FROM employees WHERE department = '{department_one}'") 
    query2 = (f"SELECT AVG(age) FROM employees WHERE department = '{department_two}'")
    cursor.execute(query1)
    average1 = cursor.fetchone()
    cursor.execute(query2)
    average2= cursor.fetchone()

    if average1 > average2:
        print("Average age of", department_one, "department employees larger then ", department_two,"department")
    elif average1 == average2:
        print("Invalid input, you chose the same departments")
    else: 
        print("Average age of", department_two, "department employees larger then", department_one,"department")

def view_with_games(cursor):
    if checkTableExists(cursor, "title_and_genre") == True:
        exit
    elif checkTableExists(cursor, "title_and_genre") == False:
        query = (f"CREATE VIEW title_and_genre AS SELECT title, genre FROM games ")
        cursor.execute(query)
    query_for_view = (f"SELECT * FROM title_and_genre")
    cursor.execute(query_for_view)
    for i in cursor:
        print("Title:",i[0],", Genre:", i[1])

def checkTableExists(cursor, tablename): #source https://stackoverflow.com/questions/17044259/python-how-to-check-if-table-exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True

    return False


def ceo_of_the_company_who_made_game(cursor):
    query = (f"SELECT title FROM games ") 
    print("List with games: ")
    cursor.execute(query)
    for i in cursor:
        print(i[0])
    game = input("Enter name of the game: ")
    query = (f"SELECT ceo FROM companies INNER JOIN games ON games.company = companies.name WHERE title = '{game}'")
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print("Name of the company's CEO who made", game,"is",result)   


def employees_who_made_the_game(cursor):
    query = (f"SELECT title FROM games ") 
    print("List with games: ")
    cursor.execute(query)
    for i in cursor:
        print(i[0])
    game = input("Enter name of the game: ")
    department = input("Enter interested department(Programming, Graphic-design, Management or All in case if you need all employees): ")
    if department == "All":
        query = (f"""SELECT employees.name FROM employees  
                     INNER JOIN games ON games.company = employees.company WHERE title = '{game}'""")
        cursor.execute(query)
        for i in cursor:
            print(i[0])
    else:
        query = (f"""SELECT employees.name FROM employees  
                     INNER JOIN games ON games.company = employees.company WHERE title = '{game}' AND department = '{department}'""")
        cursor.execute(query)
        for i in cursor:
            print(i[0])


def companies_group_by_number_of_employees(cursor):
    query = (f"SELECT name, total_employees FROM companies ORDER BY total_employees")
    cursor.execute(query)
    for i in cursor:
        print("Company:",i[0], "|  Total employees:",i[1])

def heads_of_company_departments(cursor):
    company = input("Enter name of the company(Blizzard, Valve, Ubisoft, CD projekt RED): ")
    query = (f"SELECT name, head_department FROM departments WHERE company = '{company}'")
    cursor.execute(query)
    print("Heads_of_departments:")
    for i in cursor:
        print("Department:",i[0], end=" ")
        print("Name:",i[1])