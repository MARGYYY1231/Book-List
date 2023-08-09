from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database

app = tk.Tk()
app.title('Book Reccomendation System')
app.geometry('900x420')
app.rowconfigure(0, weight=1)
app.columnconfigure(0,weight=1)
app.resizable(False,False)

def add_to_treeview():
    books = database.fetch_book()
    tree.delete(*tree.get_children())
    for book in books:
        tree.insert('', END, values=book)

def insert():
    title = title_entry.get()
    ch = chapters_entry.get()
    read = read_options.get()
    web = website_entry.get()
    rec = recommend_entry.get()

    if not(title and ch and read and web and rec):
        messagebox.showerror('Error', 'Please Enter Something in Every Field.')
    elif database.title_exists(title):
        messagebox.showerror('Error', 'It is already in your list to read.')
    else:
        database.insert_book(title, ch, read, web, rec)
        add_to_treeview()
        messagebox.showinfo('Sucess', 'You have successfully added it to you to read list.')

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        title_entry.delete(0,END)
        chapters_entry.delete(0,END)
        read_options.current(0)
        website_entry.delete(0,END)
        recommend_entry.delete(0,END)

def display_data(event):
    selected = tree.focus()
    if selected:
        row = tree.item(selected)['values']
        clear(True)
        title_entry.insert(0,row[0])
        chapters_entry.insert(0,row[1])
        read_options.set(row[2])
        website_entry.insert(0,row[3])
        recommend_entry.insert(0,row[4])

def delete():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error', 'Choose a book to remove from your list.')
    else:
        title = title_entry.get()
        database.delete_book(title)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', title + 'has been removed from your list')

def update():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error', 'Choose a book to update from your list.')
    else:
        title = title_entry.get()
        ch = chapters_entry.get()
        read = read_options.get()
        web = website_entry.get()
        rec = recommend_entry.get()
        database.update_book(ch, read, web, rec, title)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', title + 'has been updated.')

frame1 = tk.Frame(app, bg='#1974D1')
frame1.grid(row=0,column=0,sticky='nsew')

frame2 = tk.Frame(frame1, bg='#c8c5f3', highlightbackground='#c5d9f3', highlightthickness=2)
frame2.place(x=20, y=50)

title_label = tk.Label(frame2, text="Title: ", bg='#c8c5f3')
title_label.pack(padx = 20, pady = 5)
title_entry = tk.Entry(frame2)
title_entry.pack(padx = 20, pady = 5)

chapters_label = tk.Label(frame2, text="Chapters: ", bg='#c8c5f3')
chapters_label.pack(padx = 20, pady = 5)
chapters_entry = tk.Entry(frame2)
chapters_entry.pack(padx = 20, pady = 5)

read_label = tk.Label(frame2, text="Have already read: ", bg='#c8c5f3')
read_label.pack(padx = 20, pady = 5)

options = ['Read', 'Not Read', 'Reading']
var1 = StringVar()

read_options = ttk.Combobox(frame2, values=options, state='readonly')
read_options.pack(padx = 20, pady = 5)
read_options.current(0)
read_options.pack(padx=20, pady=5)

website_label = tk.Label(frame2, text="Website to read on: ", bg='#c8c5f3')
website_label.pack(padx = 20, pady = 5)
website_entry = tk.Entry(frame2)
website_entry.pack(padx = 20, pady = 5)

recommend_label = tk.Label(frame2, text="Recommended from: ", bg='#c8c5f3')
recommend_label.pack(padx = 20, pady = 5)
recommend_entry = tk.Entry(frame2)
recommend_entry.pack(padx = 20, pady = 5)

frame3 = tk.Frame(frame1, bg='#c5d9f3', highlightbackground='#c5d9f3', highlightthickness=2)
frame3.place(x=390, y=370)
for x in range(4):
    frame3.columnconfigure(x, weight=1)

add_button = tk.Button(frame3, text="ADD", command=lambda:insert())
add_button.grid(row=0, column=0, padx=20, pady=5)

clear_button = tk.Button(frame3, text="NEW", command=lambda:clear(True))
clear_button.grid(row=0, column=1, padx=20, pady=5)

update_button = tk.Button(frame3, text="UPDATE", command=lambda:update())
update_button.grid(row=0, column=2, padx=20, pady=5)

delete_button = tk.Button(frame3, text="DELETE", command=lambda:delete())
delete_button.grid(row=0, column=3, padx=20, pady=5)

frame4 = tk.Frame(frame1, bg='#c5f3c8', highlightbackground='#c5d9f3', highlightthickness=2)
frame4.place(x=250, y=30)

tree = ttk.Treeview(frame4, height=15)
tree['columns'] = ('Title', 'Chapters', 'Read', 'Website', 'Recommended')

tree.column('#0', width=0, stretch=tk.NO) #Hides te default first column
tree.column('Title', anchor=tk.CENTER, width=120)
tree.column('Chapters', anchor=tk.CENTER, width=120)
tree.column('Read', anchor=tk.CENTER, width=100)
tree.column('Website', anchor=tk.CENTER, width=120)
tree.column('Recommended', anchor=tk.CENTER, width=140)

tree.heading('Title', text='Title')
tree.heading('Chapters', text='No. Chapters')
tree.heading('Read', text='Already Read')
tree.heading('Website', text='Website to Read on')
tree.heading('Recommended', text='Recomendation From')

tree.pack()


tree.bind('<ButtonRelease>', display_data)

add_to_treeview()

app.mainloop()