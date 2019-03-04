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
import myplot
import db
import argparse
import locale
import datetime
from cryptography.fernet import Fernet

""" 

Global variables that hold configuration information such as directory
names, file names, and Oracle user name and password.

"""

# directories

config_dir = None
password_dir = None
output_dir = None

# files

password_file = 'password'
key_file = 'key'

# fixed file names

directories_file = 'directories.txt'
username_file = 'username.txt'
ashcpu_file = 'ashcpufile.txt'
groupsigs_file = 'groupofsignatures.txt'

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
        inFile = open(CFG_FILE, 'r')
    except IOError as e:
        if e.strerror == 'No such file or directory':
            source_dir = get_source_dir()
            print("File:")
            print(CFG_FILE)
            print("not found.")
            print("")
            print("Please copy "+file_name+" from")
            print(source_dir+"configfiletemplates")
            print("to")
            print(directory)
            print("and edit with your information.")
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

def get_user():
    """ 
    Get Oracle user name.
    """
    lines = read_config_file(util.config_dir,util.username_file)
    util.my_oracle_user = lines[2]
    
def load_configuration():
    """ 
    Called by the main script to get the directory and file names. Also 
    gets the name of the Oracle user. 
    """
    get_directories()
    get_user()
    
def save_key():
    """
    Generates and saves a key for password encryption and 
    decryption.
    
    Uses cryptography.fernet.
    
    """

    # Generate key
    key = Fernet.generate_key()
    
    # Save key to file
    try:
        f = open(config_dir+key_file, 'wb')
    except IOError as e:
        if e.strerror == 'No such file or directory':
            print("Could not open key file for write")
            sys.exit()
        else:
            raise e
   
    f.write(key)
    f.close()
    
def get_key():
    """
    Return key for password encryption and decryption.
    
    Uses cryptography.fernet.
    
    """
    # read key
    try:
        f = open(config_dir+key_file, 'rb')
    except IOError as e:
        if e.strerror == 'No such file or directory':
            print("Could not find key file")
            sys.exit()
        else:
            raise e
   
    key = f.read()
    f.close()
    
    return key   

def get_oracle_password():
    """
    Return my oracle password
    
    Uses cryptography.fernet to unencrypt password.
    
    """
   
    key = get_key()
    
    # read password
    try:
        f2 = open(password_dir+password_file, 'rb')
    except IOError as e:
        if e.strerror == 'No such file or directory':
            print("Could not find password file")
            sys.exit()
        else:
            raise e
    token=f2.read()
    f2.close()

    # decript password
    f = Fernet(key)
    password = f.decrypt(token).decode('utf-8')

    return password
    
def save_oracle_password(password):
    """
    Saves oracle password.
    
    Uses cryptography.fernet to unencrypt password.
    
    """

    key = get_key()
    
    # encrypt password
    f = Fernet(key)
    token = f.encrypt(password.encode('utf-8'))
    
    # write password
    try:
        f2 = open(password_dir+password_file, 'wb')
    except IOError as e:
        if e.strerror == 'No such file or directory':
            print("Could open password file for write")
            sys.exit()
        else:
            raise e
    f2.write(token)
    f2.close()
    
def input_with_default(prompt,default_value):
    if sys.version_info.major < 3:
        entered_value = raw_input('Enter '+prompt+' or press enter for default ('+default_value+'): ')
    else:
        entered_value = input('Enter '+prompt+' or press enter for default ('+default_value+'): ')
    if entered_value == "":
        return default_value
    else:
        return entered_value

def input_no_default(prompt):
    if sys.version_info.major < 3:
        entered_value = raw_input(prompt)
    else:
        entered_value = input(prompt)
    return entered_value
   
def script_startup(script_description):
    util.load_configuration()

# global variable holding database name

    database='ORCL'

    parser = argparse.ArgumentParser(description=script_description,
                                epilog="See README for more detailed help.")
    parser.add_argument('destination', choices=['file', 'screen'], 
                       help='Where to send the graph')
    parser.add_argument('database',default=None,nargs='?',
                       help='Name of the database')
    parser.add_argument('showsql', choices=['Y', 'N'], 
                       help='Show SQL that was executed (Y or N)')
    parser.add_argument('showdata', choices=['Y', 'N'], 
                       help='Show data returned by query (Y or N)')
                   
    args = parser.parse_args()

    if args.database != None:
        database = args.database.upper()
    else:
        database=util.input_with_default('database','ORCL')

    myplot.destination = args.destination
    db.showsql = args.showsql
    db.showdata = args.showdata
    
    user=util.my_oracle_user
    password=util.get_oracle_password()

# Set locale so we can test in IDLE

    locale.setlocale(locale.LC_ALL, 'C')

    return database,db.connection(user,password,database)

def exit_no_results(results):
    if results == None:
        print("No results returned")
        sys.exit()

# data saving routines

def open_save_file():
    """
    Opens a file in the same directory where we save images.
    
    Returns the file object.
    
    """
    file_name = output_dir+myplot.title+'.txt'
    # get rid of asterisks
    file_name = file_name.replace('*','')
    print("Saving data in "+file_name)
    save_file = open(file_name, 'w')
    return save_file
    
def save_string(save_file,mystring):
    """
    Writes a string to the output file.
    Converts None to 'None' and adds newline.
    The rest of the save routines call this routine to write
    strings on each line.
    """
    if mystring == None:
        mystring = 'None'
    save_file.write(mystring+'\n')
    
def save_date_times(save_file,my_date_times):
    """
    Saves a list of datatime objects. Uses repr to get a string
    representation.
    Saves number of list items first.
    """
    save_string(save_file,str(len(my_date_times)))
    for dt in my_date_times:
        save_string(save_file,repr(dt))

def save_list_list_nums(save_file,my_list_list_nums):
    """
    Saves a list of lists of floats.
    Saves the number of lists and then for each list saves
    the number of list members and the members themselves.
    """
    save_string(save_file,str(len(my_list_list_nums)))
    for l in my_list_list_nums:
        save_string(save_file,str(len(l)))
        for n in l:
           save_string(save_file,str(n)) 
           
def save_string_list(save_file,my_string_list):
    """
    Saves a list of strings starting with the number
    of list members.
    """
    save_string(save_file,str(len(my_string_list)))
    for s in my_string_list:
        save_string(save_file,s)

def close_file(save_file):
    save_file.close()

# data restoration routines

def open_restore_file(file_name):
    """
    Opens a file with saved graph data for reading.
    """
    restore_file = open(file_name, 'r')
    return restore_file
    
def restore_string(restore_file):
    """
    Reads one string taking off newlines if they exist and
    converting 'None' to None.
    """
    mystring = restore_file.readline()
    if mystring[len(mystring)-1:]=='\n':
        mystring = mystring[0:-1]
    if mystring == 'None':
        mystring = None
        
    return mystring
    
def restore_date_times(restore_file):
    """
    Returns a list of data time objects.
    Since it uses the dangerous eval function it 
    checks that the lines start with datetime.datetime as 
    they would if they were saved by the save routines.
    """
    num_entries = int(restore_string(restore_file))
    dt_list = []
    for entry in range(num_entries):
        dt_string = restore_string(restore_file)
        if dt_string[0:17] != 'datetime.datetime':
            print("Possible data corruption")
            sys.exit()
        else:
            dt_list.append(eval(dt_string))
    return dt_list        
           
def restore_list_list_nums(restore_file):
    """
    Restores a list of lists of floats
    """
    num_lists = int(restore_string(restore_file))
    list_list=[]
    for l in range(num_lists):
        new_list=[]
        list_size=int(restore_string(restore_file))
        for n in range(list_size):
           new_list.append(float(restore_string(restore_file)))
        list_list.append(new_list)
    return list_list
           
def restore_string_list(restore_file):
    """
    Restores a list of strings.
    """
    list_size = int(restore_string(restore_file))
    new_list=[]
    for n in range(list_size):
        new_list.append(restore_string(restore_file))
    return new_list
