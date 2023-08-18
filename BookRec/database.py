import sqlite3

#Creates the table
def create_table():
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS List(
                   title TEXT PRIMARY KEY,
                   chapters TEXT,
                   read TEXT,
                   website TEXT,
                   recommend TEXT)''')
    conn.commit()
    conn.close()

#Gets all the books in database
def fetch_book():
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM List')
    books = cursor.fetchall()
    conn.close()
    return books

#add a book
def insert_book(title, chapters, read, website, recommend):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO List(title, chapters, read, website, recommend) VALUES (?,?,?,?,?)', 
                   (title.lower().capitalize(), chapters, read, website, recommend))
    conn.commit()
    conn.close()

#delete a book
def delete_book(title):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM List WHERE title= ?', (title,))
    conn.commit()
    conn.close()

#updates the details of a book
def update_book( new_chapters, new_read, new_website, new_recommend, new_title):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE List SET chapters = ?, read = ?, website = ? , recommend = ? WHERE title = ?',
                   (new_chapters, new_read, new_website, new_recommend, new_title))
    conn.commit()
    conn.close()

#checks if a book exists in the database
def title_exists(title):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM List WHERE title = ?', (title.lower().capitalize(),))
    result = cursor.fetchone()
    conn.close()
    #print(result[0])
    return result is not None

def searchByRead(read):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM List WHERE read = ?', (read.lower().capitalize(),))
    allread = cursor.fetchall()
    conn.close()
    return allread

def searchByTitle(title):
    conn = sqlite3.connect('List.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM List WHERE title = ?', (title.lower().capitalize(),))
    titles = cursor.fetchall()
    for t in titles:
        print(t)
    conn.close()
    return titles

create_table()