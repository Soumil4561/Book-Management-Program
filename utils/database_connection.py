"""Creates and closes database connections

    Returns:
        _type_: _description_
"""
import sqlite3

class DC:
    """Class used for creation and closing database connections
    
        Attributes
        -----------
        host: str
            Name of the database which is to be used.
    """
    def __init__(self,host):
        self.connection = None
        self.host=host  #So that this could work for different databases.
        
    def __enter__(self):  #Enter function starts after 'with' and returns at 'as'
        self.connection=sqlite3.connect(self.host)   #creates connection here.
        return self.connection   #returns the connection signaling the start.
    
    def __exit__(self,exc_type,exc_val,exc_tb): #starts when block of comments in 'with' is over.
        if (exc_type or exc_val or exc_tb): #if any exception occurs, the connection would first be closed.
            self.connection.close()
        else:
            self.connection.commit()  #Commits and makes changes to the actual database
            self.connection.close() #Closes the connection.   