from tkinter.constants import END
import database_lib as db
import mysql.connector
from mysql.connector import errorcode
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, messagebox
import tkinter.font as tkFont

def list_games(cursor):
    query = (f"SELECT title FROM games ") 
    cursor.execute(query)
    list = ''
    for i in cursor:
        list += i[0] + '\n'
    return list

def first_query_input(cursor):
    
    result = ''
    company = e.get()
    try:
        ceo = db.company_ceo(cursor, company)
        output = f'The CEO of {company} is: {ceo}'
        print(ceo, output)
        messagebox.showinfo('Query Result', output)
        e.delete(0, END)
    except mysql.connector.Error as err:
        messagebox.showerror('Error', 'Something went wrong :(')

def second_query_input(cursor):
    dep1 = s1.get()
    dep2= s2.get()
    result = db.age_difference_between_different_departments(cursor, dep1, dep2)
    messagebox.showinfo('Query Result', result)
    entry1.delete(0, END)
    entry2.delete(0, END)

def third_query_output(cursor):
    result = db.view_with_games(cursor)
    messagebox.showinfo('Query result', result)

def fourth_query_input(cursor):
    game = s4.get()
    result = db.ceo_of_the_company_who_made_game(cursor, game)
    messagebox.showinfo('Query Result', result)
    e1.delete(0, END)

def fifth_query_input(cursor):
    game = s5.get()
    dep = s6.get()
    result = db.employees_who_made_the_game(cursor, game, dep)
    messagebox.showinfo('Query Result', result)
    e2.delete(0, END)
    e3.delete(0, END)

def sixth_query(cursor):
    result = db.companies_group_by_number_of_employees(cursor)
    messagebox.showinfo('Query Result', result)

def seventh_query(cursor):

    company = s7.get()
    result = db.heads_of_company_departments(cursor, company)
    messagebox.showinfo("Heads of Department", result)
    e4.delete(0, END)

def new_frame(frame):
    frame.tkraise()
    

cnx = mysql.connector.connect (
    host = "localhost",\
    port = "3307",
    user = "root",
    passwd = "root",
    unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',
)

DB_NAME = 'game_companies'
cursor = cnx.cursor()

try:
    cursor.execute(f"USE {DB_NAME}")
    db.initialization(cursor)
    cnx.commit()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        db.create_db(cursor, DB_NAME)
        db.initialization(cursor)
        cnx.commit()

window = tk.Tk()
window.title('Database Manager by Gabriele Marinosci')
window.geometry('800x500+300+200')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

main_font = tkFont.Font(family='Courier', size=30)

#frames initialization
main_frame = tk.Frame(window, bg='RoyalBlue4')
query_1 = tk.Frame(window, bg='RoyalBlue4')
query_2 = tk.Frame(window, bg='RoyalBlue4')
query_3 = tk.Frame(window, bg='RoyalBlue4')
query_4 = tk.Frame(window, bg='RoyalBlue4')
query_5 = tk.Frame(window, bg='RoyalBlue4')
query_6 = tk.Frame(window, bg='RoyalBlue4')
query_7 = tk.Frame(window, bg='RoyalBlue4')

frames = [main_frame, query_1, query_2, query_3, query_4, query_5, query_6, query_7]

for f in frames:
    f.grid(row=0, column=0, sticky='nsew')

#***********************MAIN MENU***************************
menu_lbl = tk.Label(main_frame, text='Database Manager v1.01', bg='RoyalBlue4', fg='white', font=main_font)
sub_lbl = tk.Label(main_frame, text='Select one of the following queries:', bg='RoyalBlue4', fg='white', font='Courier')
btn1 = tk.Button(main_frame, text='Display CEO of a given company', bg='black', fg='black', width=35, command=lambda:query_1.tkraise())
btn2 = tk.Button(main_frame, text='Average age difference between two departments', bg='dark slate blue', fg='black', width=35, command=lambda:query_2.tkraise())
btn3 = tk.Button(main_frame, text='VIEW of games', bg='dark slate blue', fg='black', width=35, command=lambda:query_3.tkraise())
btn4 = tk.Button(main_frame, text='Display the CEO of the company for a given game', bg='dark slate blue', fg='black', width=35, command=lambda:query_4.tkraise())
btn5 = tk.Button(main_frame, text='Employees who worked on given game', bg='dark slate blue', fg='black', width=35, command=lambda:query_5.tkraise())
btn6 = tk.Button(main_frame, text='Companies group by number of employees', bg='black', fg='black', width=35, command=lambda:query_6.tkraise())
btn7 = tk.Button(main_frame, text='Heads of companies departments', bg='black', fg='black', width=35, command=lambda:query_7.tkraise())
menu_lbl.pack(pady=20)
sub_lbl.pack(pady=10)
btn1.pack(pady=5)
btn2.pack(pady=5)
btn3.pack(pady=5)
btn4.pack(pady=5)
btn5.pack(pady=5)
btn6.pack(pady=5)
btn7.pack(pady=5)

#***********************FIRST QUERY***************************
lbl = tk.Label(query_1, text='Enter name of the company:\n(Companies: Blizzard, Valve, CD projekt RED, Ubisoft)', height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
s = StringVar()
e = tk.Entry(query_1, fg='black', textvariable=s)
submit_btn = tk.Button(query_1, text='Submit', fg='black', width=10, command=lambda:first_query_input(cursor))
return_btn = tk.Button(query_1, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=5)
e.pack(pady=5)
submit_btn.pack(pady=10)
return_btn.pack(pady=5)

#***********************SECOND QUERY****************************
instruction = 'Select two department to compare the average of their employees.\n(ex. Programming, Graphic-design, Management)'
lbl = tk.Label(query_2, text=instruction, height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
s1 = StringVar()
s2 = StringVar()
submit_button = tk.Button(query_2, text='Submit', fg='black', width=10, command=lambda:second_query_input(cursor))
entry1 = tk.Entry(query_2, text='First Department:', textvariable=s1)
entry2 = tk.Entry(query_2, text='Second Department:', textvariable=s2)
return_btn = tk.Button(query_2, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=10)
tk.Label(query_2, text='First Department:', bg='RoyalBlue4', fg='white').pack()
entry1.pack(pady=10)
tk.Label(query_2, text='Second Department:', bg='RoyalBlue4', fg='white').pack()
entry2.pack(pady=5)
submit_button.pack(pady=10)
return_btn.pack(pady=10)

#***********************THIRD QUERY***************************
instruction = 'Press ENTER button to display a VIEW of the games and their respective genre'
lbl = tk.Label(query_3, text=instruction, height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
enter_btn = Button(query_3, text='ENTER', fg='black', command=lambda: third_query_output(cursor))
return_btn = tk.Button(query_3, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=10)
enter_btn.pack(pady=10)
return_btn.pack(pady=20)


#***********************FOURTH QUERY****************************
lbl = tk.Label(query_4, text='Choose one of the following games:', height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
s4 = StringVar()
e1 = tk.Entry(query_4, fg='black', textvariable=s4)
submit_btn_1 = tk.Button(query_4, text='Submit', fg='black', width=10, command=lambda:fourth_query_input(cursor))
return_btn = tk.Button(query_4, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=5)
list = list_games(cursor)
tk.Label(query_4, text=list, bg='RoyalBlue4', fg='white', font='Courier').pack(pady=5)
e1.pack(pady=5)
submit_btn_1.pack(pady=10)
return_btn.pack(pady=5)


#***********************FIFTH QUERY****************************
lbl = tk.Label(query_5, text='Choose one of the following games:', height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
s5 = StringVar()
s6 = StringVar()
submit_btn_2 = tk.Button(query_5, text='Submit', fg='black', width=10, command=lambda:fifth_query_input(cursor))
e2 = tk.Entry(query_5, fg='black', textvariable=s5)
e3 = tk.Entry(query_5, fg='black', textvariable=s6)
lbl1 = tk.Label(query_5, text='Enter chosen department (Programming, Graphic-design, Management) \nor enter "All"to display all employees', bg='RoyalBlue4', fg='white', font='Courier')
lbl.pack(pady=10)
list = list_games(cursor)
tk.Label(query_5, text=list, bg='RoyalBlue4', fg='white', font='Courier').pack(pady=5)
e2.pack(pady=5)
lbl1.pack(pady=5)
e3.pack(pady=5)
submit_btn_2.pack(pady=10)
return_btn = tk.Button(query_5, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
return_btn.pack(pady=5)


#***********************SIXTH QUERY**************************
instruction = 'Press ENTER button to display companies oredered by number of total employees'
lbl = tk.Label(query_6, text=instruction, height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
enter_btn1 = Button(query_6, text='ENTER', fg='black', command=lambda: sixth_query(cursor))
return_btn = tk.Button(query_6, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=10)
enter_btn1.pack(pady=10)
return_btn = tk.Button(query_6, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
return_btn.pack(pady=20)


#***********************SEVENTH QUERY***************************
instruction = 'Enter the name of a company to display a list with the Head of each department\n(Companies: Blizzard, Valve, CD projekt RED, Ubisoft)'
lbl = tk.Label(query_7, text=instruction, height=5, bg='RoyalBlue4', fg='white', font=tkFont.Font(family='Courier', size=15))
s7 = StringVar()
e4 = tk.Entry(query_7, fg='black', textvariable=s7)
submit_btn3 = tk.Button(query_7, text='Submit', fg='black', width=10, command=lambda:seventh_query(cursor))
return_btn = tk.Button(query_7, text='Back to main menu', fg='black', width=10, command=lambda:main_frame.tkraise())
lbl.pack(pady=5)
e4.pack(pady=5)
submit_btn3.pack(pady=10)
return_btn.pack(pady=5)


main_frame.tkraise()
window.mainloop()