"""
Utility functions and classes
"""

def input_with_default(prompt,default_value):
    entered_value = raw_input('Enter '+prompt+' or press enter for default ('+default_value+'): ')
    if entered_value == "":
        return default_value
    else:
        return entered_value

class me:
    def __init__(self):
        """ read my oracle user and password from file """
        USER_FILE = "C:\mypython\myoracleuser.txt"
        inFile = open(USER_FILE, 'r', 0)
        l = inFile.read().splitlines()
        self.username = l[0]
        self.password = l[1]
        return

    def my_oracle_username(self):
        """ return my oracle username """
        return self.username
    
    def my_oracle_password(self):
        """ return my oracle password """
        return self.password
