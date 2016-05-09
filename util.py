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

Utility functions and global variables

"""

import util
import sys

""" 

Global variables that hold configuration information such as directory
names, file names, and Oracle user name and password.

"""

# directories

config_dir = None
password_dir = None
output_dir = None

# files

password_file = None

# fixed file names

directories_file = 'directories.txt'
userandfiles_file = 'userandfilenames.txt'
ashcpu_file = 'ashcpufile.txt'

# Oracle user

my_oracle_user = None

def get_source_dir():
    util_py = (util.__file__)
    file_start = util_py.find('util.py')
    source_dir = util_py[0:file_start]
    return source_dir

def read_config_file(directory,file_name):
    CFG_FILE = directory+file_name
    try:
        inFile = open(CFG_FILE, 'r', 0)
    except IOError as e:
        if e.strerror == 'No such file or directory':
            source_dir = get_source_dir()
            print "File:"
            print CFG_FILE
            print "not found."
            print ""
            print "Please copy "+file_name+" from"
            print source_dir+"configfiletemplates"
            print "to"
            print directory
            print "and edit with your information."
            sys.exit()
        else:
            raise e
        
    lines = inFile.read().splitlines()
    inFile.close()
    return lines

def get_directories():
    """ 
    Get directory names from a file that is in the same
    directory as the source code.
    """
    
    source_dir = get_source_dir()
    lines = read_config_file(source_dir,util.directories_file)
    util.config_dir = lines[2]
    util.password_dir= lines[3]
    util.output_dir= lines[4]

def get_user_and_files():
    """ 
    Get Oracle user name and file names.
    """
    lines = read_config_file(util.config_dir,util.userandfiles_file)
    util.my_oracle_user = lines[3]
    util.password_file = lines[4]
    
def load_configuration():
    """ 
    Called by the main script to get the directory and file names. Also 
    gets the name of the Oracle user. 
    """
    get_directories()
    get_user_and_files()

def get_oracle_password(database):
    """
    Return my oracle password
    
    This assumes that the password file has entries of the format
    
    database:username:password
    
    Also, if database is ALLDBS, then it assumes that all databases
    have the same password for the given user.
    
    """
    lines = read_config_file(util.password_dir,util.password_file)
    # look for specific database first
    for oneline in lines:
        if oneline[0] <> '#':
            fields = oneline.split(':')
            if fields[0].upper() == database.upper() and fields[1].upper() == util.my_oracle_user.upper():
                return fields[2]
    # look for ALLDBS indicating same password all databases
    for oneline in lines:
        if oneline[0] <> '#':
            fields = oneline.split(':')
            if fields[0].upper() == 'ALLDBS' and fields[1].upper() == util.my_oracle_user.upper():
                return fields[2]
    
def input_with_default(prompt,default_value):
    entered_value = raw_input('Enter '+prompt+' or press enter for default ('+default_value+'): ')
    if entered_value == "":
        return default_value
    else:
        return entered_value
   