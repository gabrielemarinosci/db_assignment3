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

def company_ceo(cursor, company):
    query = (f"SELECT ceo FROM companies WHERE name = '{company}'") 
    cursor.execute(query)
    result = ''
    for i in cursor:
        result += i[0] + '\n';
    return result

def age_difference_between_different_departments(cursor, first_dep, second_dep):
    query1 = (f"SELECT AVG(age) FROM employees WHERE department = '{first_dep}'") 
    query2 = (f"SELECT AVG(age) FROM employees WHERE department = '{second_dep}'")
    cursor.execute(query1)
    average1 = cursor.fetchone()
    cursor.execute(query2)
    average2= cursor.fetchone()

    if average1 > average2:
        result = f'Average age of {first_dep} ({average1} is greater than {second_dep} ({average2}))'
        return result
    elif average1 == average2:
        result = "Invalid input, you chose the same departments"
        return result
    else: 
        result = f'Average age of {second_dep} ({average2} is greater than {second_dep} ({average1}))'
        return result
        
def checkTableExists(cursor, tablename): #source https://stackoverflow.com/questions/17044259/python-how-to-check-if-table-exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True

    return False

def view_with_games(cursor):
    if checkTableExists(cursor, "title_and_genre") == True:
        exit
    elif checkTableExists(cursor, "title_and_genre") == False:
        query = (f"CREATE VIEW title_and_genre AS SELECT title, genre FROM games ")
        cursor.execute(query)
    query_for_view = (f"SELECT * FROM title_and_genre")
    cursor.execute(query_for_view)
    result = ''
    for i in cursor:
        #print("Title:",i[0],", Genre:", i[1])
        result += f'Title: {i[0]}  Genre: {i[1]}\n'
    return result

def ceo_of_the_company_who_made_game(cursor, game):

    query = (f"SELECT ceo FROM companies INNER JOIN games ON games.company = companies.name WHERE title = '{game}'")
    cursor.execute(query)
    result = cursor.fetchone()[0]
    record = f'Name of the CEO of the company that made {game} is: {result}'
    return record

def employees_who_made_the_game(cursor, game, department):
    if department == "All":
        query = (f"""SELECT employees.name FROM employees  
                     INNER JOIN games ON games.company = employees.company WHERE title = '{game}'""")
        cursor.execute(query)
        result = ''
        for i in cursor:
            result += i[0] + '\n'
    else:
        query = (f"""SELECT employees.name FROM employees  
                     INNER JOIN games ON games.company = employees.company WHERE title = '{game}' AND department = '{department}'""")
        cursor.execute(query)
        result = ''
        for i in cursor:
            result += i[0] + '\n'
    
    return result

def companies_group_by_number_of_employees(cursor):
    query = (f"SELECT name, total_employees FROM companies ORDER BY total_employees")
    cursor.execute(query)
    result = ''
    for i in cursor:
        result += f'Company: {i[0]}  |  Total employees: {i[1]}\n'
    return result

def heads_of_company_departments(cursor, company):
    query = (f"SELECT name, head_department FROM departments WHERE company = '{company}'")
    cursor.execute(query)
    result = ''
    for i in cursor:
        result += f'Department: {i[0]}  |  Name: {i[1]}\n'
    return result