import utils.database as database
from collections import Counter
from datetime import datetime, timedelta,timezone
import utils.front_export_import as transfer

def lib_add_book(lib_name)->None:
    """Calls function from module to add a book"""
    name = input("Enter Book name: ").strip().lower().title()      #Entering Details
    author=input("Enter Author name: ").strip().lower().title()
    time=datetime.now(timezone.utc)
    time=time+timedelta(hours=5.30)
    date=time.strftime("%d/%m/%Y")
    time=time.strftime("%H:%M:%S")
    database.write_to_file(name,author,date,time,lib_name)     #calls write_to_file function from module

def lib_list_books(lib_name)->None:
    """Calls function from module to list all books"""
    metadata = database.get_all_books(lib_name)
    for counter, dic in enumerate(metadata,start=1): #printing each book detail one by one
        print(f"""\n{counter}. Book name: {dic['Title']}       
   Author:{dic['Author']}
   Read: {dic['Read']}
   Date Added: {dic['Date']}
   Time: {dic['Time']}\n""")

def lib_change_status_book(lib_name)->None:
    """Calls function from module to change read statuts to yes."""
    name = input("Enter Book name: ").strip().lower().title()
    author=input("Enter Author name: ").strip().lower().title()
    status= input(f"Have you read {name}? (y/n): ").strip().lower()
    database.change_read_status(name,author,status,lib_name)
    
def lib_delete_book(lib_name)->None:
    """Function for deleting books from database."""
    name = input("Enter Book name: ").strip().lower().title()
    author=input("Enter Author name: ").strip().lower().title()
    database.delete_from_file(name,author,lib_name)
        
def delete_table(lib_name):
    ques=input(f"\nIt is advisable to first export your data before deletion of library.\nAre you sure you wish to delete library '{lib_name}'?(y/n)")
    if ques=='y':
        database.delete_table(lib_name)
    elif ques=='n':
        print("Going back to main menu.\n")
    else:
        print("Invalid Option. Going Back...\n")
         
def lib_functions(lib_name):
    i=0
    while i != 'q':
            database.menu_counter(lib_name)   #for showing current status of the books in that library.
            print("""Enter an option:
            a: Add a book.
            l: list all books.
            r: Change read status of a book.
            f: Export or Import books.
            d: Delete a book.
            b: Go Back.""")
            i = input("Your choice: ")
            if i == 'a':
                lib_add_book(lib_name)
            elif i == 'l':
                lib_list_books(lib_name)
            elif i == 'r':
                lib_change_status_book(lib_name)
            elif i == 'd':
                lib_delete_book(lib_name)
            elif i=='f':
                try:
                    q=int(input(f"""Enter Choice:\n1. Export from {lib_name}\n2. Import to {lib_name}\n\nYour Choice: """))
                except ValueError:
                    print("Invalid value, Going back...")
                else:
                    if (q==1):
                        transfer.export_format([],lib_name,True)
                    elif (q==2):
                        filename,filepath=transfer.check_import_path();
                        transfer.import_format(filename,filepath,lib_name,True)
                    else:
                        print("Invalid option. Going back...")
            elif i == 'b':
                break
            else:
                print("Invalid option try again")
                break
            i = input("""To go back to library menu, enter m\nTo go back to main menu, enter b: """)
            if i == 'm':
                continue
            elif i == 'q':
                print("Goodbye!")
                break
            else:
                print("Invalid option, going back to main menu.")
                break

def menu()->None:
    j='n'
    try:
        j=input("").strip().lower()
    except Exception:
        pass
    else:
        while j=='y':
            j='n'
            libraries=database.readtables()
            if len(libraries)==0:
                ques=input("\nNo libraries found. Would you like to create one?(y/n): ")
                if ques=='y':
                    lib_name=input("\nEnter library name: ").strip().lower().title()
                    database.create_book_table(lib_name)
                    j='y'
                elif ques=='n':
                    print("Library will be created under the name 'Library'.")
                    database.create_book_table()
                    j='y'
                else:
                    print("Invalid Option. Exiting Program.")

            else:
                try:
                    x=int(input("""What do you want to do:\n
                        1. Make new library.
                        2. Access Current Libraries
                        3. Delete a library
                        4. Export or Import Data
                        5. List all books in each library and display in tree format.
                        6. Quit Program.
                        
                        Your Choice: """))
                except ValueError:
                    print("Please enter integer values from 1 to 6.")
                    j='y'
                else:
                    if x==1:
                        lib_name=input("Enter name of library: ").strip().lower().title()
                        if lib_name in libraries:
                            print("Library already found in Database.")
                        else:
                            if(database.create_book_table(lib_name)): 
                                print("\nLibrary successfully created\n")
                        j='y'
                    elif x==2:
                        print("\nEnter nummber next to library which you wish to use")
                        [print(f"{counter}. {name}") for counter,name in enumerate(libraries,start=1)]
                        try:
                            lib=int(input("Your Choice: "))
                            lib_functions(libraries[lib-1])
                        except IndexError:
                            print('Please choose from the given options only!')
                        except ValueError:
                            print("Only integer values please.")
                        finally:
                            j='y'
                    elif x==3:
                        print("\nEnter nummber next to library which you wish to delete.")
                        [print(f"{counter}. {name}") for counter,name in enumerate(libraries,start=1)]
                        try:
                            lib=int(input("Your Choice: "))
                            delete_table(libraries[lib-1])
                        except IndexError:
                            print('Please choose from the given options only!')
                        except ValueError:
                            print("Only integer values please.")
                        finally:
                            j='y'
                    elif x==4:
                        transfer.query(libraries)
                        j='y'
                    elif x==5:
                        database.make_lib_tree(libraries)
                        j='y'
                    elif x==6:
                        print("Goodbye!")
                    else:
                        print("Invalid Option entered. Exiting Program.")
                
if __name__=='__main__':
    print("Welcome to Alpha Book Management Program. To start enter y: ")
    menu()