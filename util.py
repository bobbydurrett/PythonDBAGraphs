"""
PythonDBAGraphs: Graphs to help with Oracle Database Tuning
Copyright (C) 2016  Robert Taft Durrett (Bobby Durrett)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact:

bobby@bobbydurrettdba.com

util.py

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
