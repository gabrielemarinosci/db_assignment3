import tkinter as tk

win = tk.Tk()
canvas = tk.Canvas(win, width=1000, height=1000)


query1 = tk.Button(
    text='This is the first query',
    width=25,
    height=1,
    bg='black',
    fg='black'
)

query1.pack()
canvas.pack()

win.mainloop()