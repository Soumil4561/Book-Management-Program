import utils.back_export_import as bex

#Database basis
#Library basis

def query(libraries):
    try:
        ques1=int(input("""\nDo you want to: 
        1. Export Data
        2. Import Data\nYour Choice: """))
    except ValueError:
        print("Please enter only integer values as per you choice.")
    else:
        if ques1==1:
            try:
                ques2=int(input("""Do you want to:
            1. Export entire database.
            2. Export only select libraries from the database\nYour Choice: """))
            except ValueError:
                print("Only integer inputs valid.")
            else:
                if ques2==1:
                    export_format(libraries)
                
                elif ques2==2:
                    print("Enter numbers next to the libraries in space seperated format")
                    [print(f"{counter}. {a}") for counter,a in enumerate(libraries,start=1)]
                    ch=[int(a) for a in input("Your Choice: ").split() if a.isnumeric()]
                    try:
                        select_libs=[libraries[i-1] for i in ch]
                    except IndexError:
                        print("Invalid entries. Going Back..")
                   
                    else:
                        export_format(select_libs)
                
                else:
                    print("Invalid option entered. Going back...")
            
        elif ques1==2:
            filename,filepath=check_import_path()
            print("""Which library do you wish to store these books?
    1. In the libraries specified in the file.""")
            for counter,lib_name in enumerate(libraries,start=2):
                print(f"{counter}. In {lib_name}")
            try:
                q=int(input("Your Choice: "))
            except ValueError:
                print("Only integer inputs valid.")
            else:
                if (q==1):
                    import_format(filename,filepath)
                else:
                    try:
                        import_format(filename,filepath,libraries[q-2],True)
                    except IndexError:
                        print("Invalid option. Going Back...")
                
        else:
            print("Invalid option. Going Back...")
        
def check_export_path():
    t=0
    while(t==0):
        try:
            path=input("Enter the path where you wish for the file to be exported: ")
            bex.os.chdir(path)
        except FileNotFoundError:
            print("Entered path not found\nTry Again\n")
        else:
            t=1
            bex.os.chdir(bex.og_path)
            return path

def check_import_path():
    t=0
    while(t==0):
        try:
            path=input("Enter the path from where you wish for the file to be imported: ")
            bex.os.chdir(path)
        except FileNotFoundError:
            print("Entered path not found\nTry Again\n")
        else:
            t=1
    dir_list=bex.os.listdir(path)
    print("Select number next to the file from which data is to be imported: ")
    for counter,i in enumerate(dir_list,start=1):
        print(f"{counter}. {i}")
    while(t==1):
        try:        
            x=int(input("\nYour Choice: "))
        except ValueError:
            print("Please enter integer values only.\nTry Again")
        else:
            t=0
    for counter,i in enumerate(dir_list,start=1):
        if counter==x:
            filename=i
            break
    return filename,path

def export_format(libraries,lib_name=None,single=False):
    ques=int(input("""Select export format:
    1. Text File(.txt)
    2. CSV File(.csv)
    3. JSON file(.json)
    4. DataBase File(.db)\nYour Choice: """))
    format_dic={1:bex.txte,2:bex.csve,3:bex.jsone,4:bex.dbe}
    if ques==1 or 2 or 3 or 4:
        name=input("Enter file name: ")
        path=check_export_path()
        format=format_dic[ques]
        if (single):
            format(name,path,lib_name)
        else:
            for lib_name in libraries:
                format(name,path,lib_name)
    else:
        print("Invalid option Entered. Going back.")
        
def import_format(filename,filepath,lib_name=None,custom=False):
    try:
        ques=int(input("""Select import format:
        1. CSV File(.csv)
        2. JSON file(.json)
        3. DataBase File(.db)\nYour Choice: """))
        format_dic={1:bex.csvi,2:bex.jsoni,3:bex.dbi}
    except ValueError:
        print("Only integer inputs are valid.")
    else:
        if ques==1 or 2 or 3:
            format=format_dic[ques]
            if (custom):
                format(filename,filepath,lib_name,custom)
            else:
                format(filename,filepath)
        else:
            print("Invalid option Entered. Going back.")