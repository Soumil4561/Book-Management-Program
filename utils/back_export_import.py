"""
    This module deals with the exporting and importing
    of data from the database.
"""

import json
import csv
import sqlite3
from .database_connection import DC
from utils.database import get_all_books
from utils.database import write_to_file
import os
# do csv, db, json, txt,etc.

global og_path
og_path=os.getcwd()

class pathfinder:
    def __init__(self,filepath) -> None:
        self.filepath=filepath
    
    def __enter__(self):
        os.chdir(self.filepath)
        
    def __exit__(self,exc_tb,exc_val,exc_type): 
        os.chdir(og_path)

def export_import(lib_name):
    x=int(input("""\n   Enter 1 to export data.
    Enter 2 to import data.

Your Choice: """))
    if x==1:
        export_file(lib_name)
    elif x==2:
        import_file()
    else:
        print("\nIncorrect option entered.\n")

def export_file(lib_name):
    exp_dic={1:txte,2:csve,3:jsone,4:dbe}
    x=int(input("""\nIn which format do you want to export data from database:
    Enter 1 for text file
    Enter 2 for csv file
    Enter 3 for json file
    Enter 4 for database file
    Your Choice: """))
    try:
        function=exp_dic[x]
    except KeyError:
        print("\nEntered value not available.")
    else:
        filename,path=function(lib_name)
        print(f"\nFile Generated and stored in {path} as {filename}\n")
        
def export_path():
    t=0
    while(t==0):
        try:
            path=input("Enter the path where you wish for the file to be exported.")
            os.chdir(path)
        except FileNotFoundError:
            print("Entered path not found\nTry Again\n")
        else:
            t=1
            return path
        
def txte(file_name,file_path,lib_name)-> None:
    file_name+=".txt"
    data=get_all_books(lib_name)
    lst=[((f"""{counter}. Book name: {dic['Title']}       
Author:{dic['Author']}
Read: {dic["Read"]}
Date Added: {dic['Date']}
Time: {dic['Time']}\n\n"""))for counter,dic in enumerate(data,start=1)]
    
    with pathfinder(file_path) as path:
        with open(file_name,'a') as file:
            file.write(lib_name)
            file.writelines(lst)
    return file_name,file_path
        
def csve(file_name,file_path,lib_name):
    file_name+=".csv"
    data=get_all_books(lib_name)
    with pathfinder(file_path) as path:
        with open(file_name,'a',newline="") as file:
            writer=csv.DictWriter(file,fieldnames=["Library","Title","Author","Read","Date","Time"],delimiter='|')
            writer.writeheader()
            writer.writerows(data)
    return file_name,file_path

def jsone(file_name,file_path,lib_name):
    file_name+=".json"
    data=get_all_books(lib_name)
    with pathfinder(file_path) as path:
        with open(file_name,'a') as file:
            json.dump(data,file,indent=4)
    return file_name,file_path
    
def dbe(file_name,file_path,lib_name):
    file_name+=".db"
    data=get_all_books(lib_name)
    with pathfinder(file_path) as path:
        with DC(file_name) as connection:
            cursor=connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {lib_name}(S_No INTEGER PRIMARY KEY, Title TEXT,Author TEXT, Date_Added TEXT, Time TEXT, Read_Status TEXT)")
            for counter,book in enumerate(data,start=1):
                try:
                    cursor.execute(f"INSERT INTO {lib_name} VALUES(?,?,?,?,?,?)",(counter,book["Title"],book["Author"],book['Date'],book["Time"],book["Read"]))
                except sqlite3.IntegrityError:
                    print(f"A book database is already in directory in {file_path}. Kindly delete or move that file to generate a new one here.")
                    error=1
                    break
    return file_name,file_path

def import_file():
    imp_dic={1:csvi,2:jsoni,3:dbi}
    x=int(input("""
    In which format do you want to import data to database:
    Enter 1 for csv file
    Enter 2 for json file
    Enter 3 for database file
    Your Choice: """))
    try:
        function=imp_dic[x]
    except KeyError:
        print("\nEntered value not availabe.")
    else:
        filename=function()
        print(f"\nData imported from {filename} and stored in database.\n")

def csvi(file_name,file_path,lib_name=None,custom=False):
    with pathfinder(file_path) as path:
        with open(file_name,'r') as file:
            file_contents=file.readlines()
            content=[]
            for book in file_contents:
                data=book.split("|")
                try:
                    if (data[1]=='Title' and data[2]=='Author'):
                        continue
                except IndexError:
                    print("Encountered error while parsing file. Please recheck file format.")
                else:
                    content.append(data)
    if (custom):
        try:
            for book in content:
                write_to_file(book[1],book[2],book[4],book[5],lib_name,book[3])
        except Exception:
            print("Encountered error while parsing file. Please recheck file format.")
    else:
        try:
            for book in content:
                write_to_file(book[1],book[2],book[4],book[5],book[0],book[3])
        except Exception:
            print("Encountered error while parsing file. Please recheck file format.")
        
def jsoni(file_name,file_path,lib_name=None,custom=False):
    os.chdir(og_path)
    with open(file_name,'r') as file:
        file_contents=json.load(file)
        if (custom):
            try:
                for book in file_contents:
                    write_to_file(book['Title'],book['Author'],book['Date'],book['Time'],lib_name,book['Status'])
            except Exception:
                print("Encountered error while parsing file. Please recheck file format.")
        
        else:
            try:
                for book in file_contents:
                    write_to_file(book['Title'],book['Author'],book['Date'],book['Time'],book["Library"],book['Status'])
            except Exception:
                 print("Encountered error while parsing file. Please recheck file format.")
                 
def dbi(file_name,file_path,lib_name=None,custom=False):
    with DC(file_name) as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT name From sqlite_master where type='table'")
        lib_list=[name[0] for name in cursor.fetchall()]
        for lib in lib_list:
            cursor.execute(f"SELECT * FROM {lib}")
            file_contents=[{'Title':row[1],'Author':row[2],'Date':row[3],'Time':row[4],'Read':row[5]} for row in cursor.fetchall()]
            os.chdir(og_path)
            if (custom):
                try:
                    for book in file_contents:
                        write_to_file(book['Title'],book['Author'],book['Date'],book['Time'],lib_name,book['Read'])
                except Exception:
                    print("Encountered error while parsing file. Please recheck file format.")
                
            else:
                try:
                    for book in file_contents:
                        write_to_file(book['Title'],book['Author'],book['Date'],book['Time'],lib,book['Read'])
                except Exception:
                    print("Encountered error while parsing file. Please recheck file format.")
            os.chdir(file_path)
    os.chdir(og_path)