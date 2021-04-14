from tkinter import *
import requests
import json
import sqlite3

todo = Tk()
todo.title("To-Do List")
todo.iconbitmap("favicon.ico")

con = sqlite3.connect('task.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY, task_name TEXT, status TEXT)")
con.commit()

#cursorObj.execute("INSERT INTO task(task_name, status) VALUES(?, ?)",("Homework","Pending"))
#cursorObj.execute("INSERT INTO task(task_name, status) VALUES(?, ?)",("Coding","Done"))
#cursorObj.execute("INSERT INTO task(task_name, status) VALUES(?, ?)",("Assignment","Pending"))
#con.commit()

def reset():
    for cell in todo.winfo_children():
        cell.destroy() 
    header()
    todolist()
  
def todolist():

    def color(status):
        if status == "Done":
            return "green"
        else:
            return "red"

    def pending(button):
        x=button.grid_info()['row']
        button.grid_forget()
        id = tasks[x-1][0]
        cursorObj.execute("UPDATE task SET status=? WHERE id=?",("Pending",id))
        con.commit()
        reset()
        
    def done(button):
        x=button.grid_info()['row']
        button.grid_forget()
        id = tasks[x-1][0]
        cursorObj.execute("UPDATE task SET status=? WHERE id=?",("Done",id))
        con.commit()
        reset()

    def to_delete(button):
        x=button.grid_info()['row']
        button.grid_forget()
        id = tasks[x-1][0]
        cursorObj.execute("DELETE FROM task WHERE id=?",(id,))
        con.commit()
        reset()

    def to_add():
        cursorObj.execute("INSERT INTO task(task_name, status) VALUES(?, ?)",(new_task.get(),"Pending"))
        con.commit()
        reset()
        
    cursorObj.execute("SELECT * FROM task")
    tasks = cursorObj.fetchall()

    current_row = 1

    for task in tasks:
        fg_color = color(task[2])
        task_id = Label(todo, text=current_row, fg=fg_color, width="10", padx="5", pady="5", font="Lato 10")
        task_id.grid(row = current_row, column = 0)

        task_name = Label(todo, text=task[1], fg=fg_color, width="25", padx="5", pady="5", font="Lato 10")
        task_name.grid(row = current_row, column = 1)

        task_status = Label(todo, text=task[2], fg=fg_color, padx="5", pady="5", font="Lato 10")
        task_status.grid(row = current_row, column = 2)

        if task[2] == "Done":
            task_change = Button(todo, text="Mark as Pending", bg="#00abf0", fg="#ffffff", width="15", padx="5", pady="5", font="Lato 10")
            task_change.configure(command=lambda button=task_change: pending(button))
            task_change.grid(row = current_row, column = 3)
        else:
            task_change = Button(todo, text="Mark as Done", bg="#00abf0", fg="#ffffff", width="15", padx="5", pady="5", font="Lato 10")
            task_change.configure(command=lambda button=task_change: done(button))
            task_change.grid(row = current_row, column = 3)
    
        task_delete = Button(todo, text="Delete", bg="red", fg="#ffffff", padx="5", pady="5", font="Lato 10")
        task_delete.configure(command=lambda button=task_delete: to_delete(button))
        task_delete.grid(row = current_row, column = 4)

        
        current_row += 1

    add = Label(todo, text="New Task", bg="#333333", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove", width="10")
    add.grid(row = current_row, column = 0)

    new_task = Entry(todo, borderwidth=2, relief="groove", width="25")
    new_task.grid(row = current_row, column = 1)

    add_task =Button(todo, text="Add", command = to_add, bg="#00abf0", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove")
    add_task.grid(row = current_row, column = 2) 

def header():
    task_id = Label(todo, text="Task Number", bg="#333333", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove", width="10")
    task_id.grid(row = 0, column = 0)

    task_name = Label(todo, text="Task", bg="#333333", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove", width="25")
    task_name.grid(row = 0, column = 1)

    task_status = Label(todo, text="Status", bg="#333333", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove")
    task_status.grid(row = 0, column = 2)

    task_change = Label(todo, text="Change Status", bg="#333333", fg="#ffffff", width="15", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove")
    task_change.grid(row = 0, column = 3)

    task_delete = Label(todo, text="Delete", bg="#333333", fg="#ffffff", font="Lato 12 bold", padx="5", pady="5", borderwidth="2", relief="groove")
    task_delete.grid(row = 0, column = 4)

 
header()
todolist()

todo.mainloop()

cursorObj.close()
con.close()

