from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database

#Create the window
app = tk.Tk()
app.title('Book Reccomendation System')
app.geometry('900x420')
app.rowconfigure(0, weight=1)
app.columnconfigure(0,weight=1)
app.resizable(False,False)

#Get the search type
def searchType():
    global pop
    pop = Toplevel(app)
    pop.title("Type of search")
    pop.geometry("250x150")
    pop_Label = tk.Label(pop, text="Search By: ")
    pop_Label.pack(pady=10)

    v = IntVar()
    v.set("1")
    Radiobutton(pop, text="Title", variable=v, value=1).pack()
    Radiobutton(pop, text="Chapter Range", variable=v, value=2).pack()
    Radiobutton(pop, text="Read Status", variable=v, value=3).pack()

    enter_button = tk.Button(pop, text="ENTER", command=lambda:search(v.get()))
    enter_button.pack()

#Search By title
def titleSearch():
    print("1 is printed")
    spop.title("Search By Title")
    title_search = tk.Label(spop, text="Enter Title: ")
    title_search.pack()
    title_search_entry = tk.Entry(spop)
    title_search_entry.pack()
    enter_button = tk.Button(spop, text="ENTER", command=lambda:add_title_to_treeview(title_search_entry.get().lower().capitalize()))
    enter_button.pack()
    title_entry.delete(0,END)
    
#Adding the one with th matching title into the treeview
def add_title_to_treeview(t):
    titles = database.searchByTitle(t)
    clear_treeview()
    for title in titles:
        tree.insert('', END, values=title)
    spop.destroy()

def search(num):
    pop.destroy()

    global spop
    spop = Toplevel(app)
    spop.geometry("250x150")
    if num == 1:
        titleSearch()

    
#Clears the treeview
def clear_treeview():
    for item in tree.get_children():
        tree.delete(item)

#Add information to table
def add_to_treeview():
    clear_treeview()
    books = database.fetch_book()
    tree.delete(*tree.get_children())
    for book in books:
        tree.insert('', END, values=book)

#Gets the users input in the text fields
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
    clear(True)

#Clears all the entry boxes
def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        title_entry.delete(0,END)
        chapters_entry.delete(0,END)
        read_options.current(0)
        website_entry.delete(0,END)
        recommend_entry.delete(0,END)

#If an entry has been clicked on puts the details in entry boxes
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

#Deletes an entry
def delete():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error', 'Choose a book to remove from your list.')
    else:
        title = title_entry.get()
        database.delete_book(title)
        add_to_treeview()
        clear(True)
        messagebox.showinfo('Success', title + 'has been removed from your list')

#Updates an entry
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
        clear(True)
        messagebox.showinfo('Success', title + 'has been updated.')

#Frame for the whole window
frame1 = tk.Frame(app, bg='#1974D1')
frame1.grid(row=0,column=0,sticky='nsew')

#===========Frame for Input Fields Area===============================
frame2 = tk.Frame(frame1, bg='#c8c5f3', highlightbackground='#c5d9f3', highlightthickness=2)
frame2.place(x=20, y=50)

#Title of the book
title_label = tk.Label(frame2, text="Title: ", bg='#c8c5f3')
title_label.pack(padx = 20, pady = 5)
title_entry = tk.Entry(frame2)
title_entry.pack(padx = 20, pady = 5)

#The number of chapters
chapters_label = tk.Label(frame2, text="Chapters: ", bg='#c8c5f3')
chapters_label.pack(padx = 20, pady = 5)
chapters_entry = tk.Entry(frame2)
chapters_entry.pack(padx = 20, pady = 5)

#Combobox to ask if the book is being read
read_label = tk.Label(frame2, text="Have already read: ", bg='#c8c5f3')
read_label.pack(padx = 20, pady = 5)

options = ['Read', 'Not Read', 'Reading']
var1 = StringVar()

read_options = ttk.Combobox(frame2, values=options, state='readonly')
read_options.pack(padx = 20, pady = 5)
read_options.current(0)
read_options.pack(padx=20, pady=5)

#Asks for the website that it could be read on
website_label = tk.Label(frame2, text="Website to read on: ", bg='#c8c5f3')
website_label.pack(padx = 20, pady = 5)
website_entry = tk.Entry(frame2)
website_entry.pack(padx = 20, pady = 5)

#Asks for where the recommendation came from
recommend_label = tk.Label(frame2, text="Recommended from: ", bg='#c8c5f3')
recommend_label.pack(padx = 20, pady = 5)
recommend_entry = tk.Entry(frame2)
recommend_entry.pack(padx = 20, pady = 5)

#==============Frame For the buttons==================================

frame3 = tk.Frame(frame1, bg='#c5d9f3', highlightbackground='#c5d9f3', highlightthickness=2)
frame3.place(x=390, y=370)
for x in range(5):
    frame3.columnconfigure(x, weight=1)

#Add button used to add a book entry
add_button = tk.Button(frame3, text="ADD", command=lambda:insert())
add_button.grid(row=0, column=0, padx=20, pady=5)

#Clear button used to clear text field
clear_button = tk.Button(frame3, text="NEW", command=lambda:clear(True))
clear_button.grid(row=0, column=1, padx=20, pady=5)

#Update button used to update a book entry
update_button = tk.Button(frame3, text="UPDATE", command=lambda:update())
update_button.grid(row=0, column=2, padx=20, pady=5)

#Deletes a book entry
delete_button = tk.Button(frame3, text="DELETE", command=lambda:delete())
delete_button.grid(row=0, column=3, padx=20, pady=5)

search_button = tk.Button(frame3, text="SEARCH", command=lambda:searchType())
search_button.grid(row=0, column=4, padx=20, pady=5)

#==========Frame for the table==============================================
frame4 = tk.Frame(frame1, bg='#c5f3c8', highlightbackground='#c5d9f3', highlightthickness=2)
frame4.place(x=250, y=30)

#Creates the table on Tkinter using treeview
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
