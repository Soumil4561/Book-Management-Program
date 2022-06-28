"""Creates, stores and updates the database of books

    Returns:
        _type_: _description_
"""
import sqlite3
from .database_connection import DC
import os

def create_book_table(lib_name="Library") -> None:
    """Function to create the table inside database."""
    with DC('database.db') as connection:   #Context Manager used for opening and closing database.
        cursor=connection.cursor()
        try:
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {lib_name}(Title TEXT PRIMARY KEY, Author TEXT, Date_Added TEXT, Time TEXT, Read_Status TEXT)")
        except sqlite3.OperationalError:
            print("Encountered some problem with creating library under this name. Try a different name.")
            return False
        else:
            return True
            
def write_to_file(name,author,date,time,lib_name,status='No') -> None:
    """Function for inserting new entries to the table."""
    create_book_table(lib_name)
    if (check_book(name,author,lib_name)):
        print(f"\n{name} by {author} already found in the {lib_name}.\n")
    else:
        with DC('database.db') as connection:
            cursor=connection.cursor()
            cursor.execute(f'INSERT INTO {lib_name} VALUES(?,?,?,?,?)',(name,author,date,time,status))
        print(f"\n{name} by {author} added successfully in {lib_name}.\n") 

def get_all_books(lib_name):
    """Function returns all books in the form of a list of dictionary 
    all containing details of all books entered in the database."""
    with DC("database.db") as connection:
        cursor=connection.cursor()
        cursor.execute(f"SELECT * FROM {lib_name}")
        books=[{'Library':lib_name,'Title':row[0],'Author':row[1],'Date':row[2],'Time':row[3],'Read':row[4]} for row in cursor.fetchall()]
    return(books)

def delete_from_file(name,author,lib_name)->None:
    """Functions for removing requested entries from library"""
    if check_book(name,author,lib_name):
        with DC("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute(f"DELETE FROM {lib_name} where Title=? and Author=?",(name,author))  
        print("\nBook successfully deleted.\n")  
    else:
        print("\nSorry! Book not found. Please try again.\n")
        
def change_read_status(name,author,status,lib_name)->None:
    """Function for changing read status to yes for the books which the user have read."""
    y=("Yes" if status=='y' else "No")  #Used for printing final response.
    if check_book(name,author,lib_name):
        with DC("database.db") as connection:
            cursor=connection.cursor()
            cursor.execute(f"UPDATE {lib_name} SET Read_Status=? WHERE Title=? and Author=?",(y,name,author))
            print(f"\nRead status Changed to {y}.\n") 
    else:
        print("\nSorry! Book not found. Please try again.\n")          

def check_book(name,author,lib_name)-> bool:
    """This function checks whether an entered is already present in the library."""
    books=get_all_books(lib_name)
    for dic in books:
        if dic['Title']==name and dic['Author']==author:
            return True      
            break
    else:
        return False 

def menu_counter(lib_name)-> None:
    """Displays total number of books and number of books read in that library."""
    books=get_all_books(lib_name)
    total=len(books)
    counter=0
    for dic in books:
        if dic['Read'] == "Yes":
            counter=counter+1
    print(f"\nTotal Number of Books in {lib_name}: {total}\nNumber of Books Read: {counter}\n")
    
def readtables():
    """Reads number of tables (or 'libraries') in the database.
    """
    with DC("database.db") as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT name From sqlite_master where type='table'")
        lib_list=[name[0] for name in cursor.fetchall()]
        print(f"\nNumber of libraries= {len(lib_list)}")
        return lib_list

def delete_table(lib_name):
    """"Deletes the table in the database and all the books along with it."""
    with DC("database.db") as connection:
        cursor=connection.cursor()    
        cursor.execute(f"DROP TABLE IF EXISTS {lib_name}")
    print(f"Library '{lib_name}' deleted successfully!\n")
    
def make_lib_tree(libraries):
    print("\nGenereatiing Tree...\n")
    for lib in libraries:
        books=get_all_books(lib)
        print(lib)
        for book in books:
            print(f"|---> {book['Title']} ({book['Author']})")
            print(f"|      |---> {book['Time']} {book['Date']}")
        print("|")