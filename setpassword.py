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

setpassword.py

Prompts for password and stores encryption key and encrypted password.

"""

import util
import getpass

# Get configuration directories

util.get_directories()

# Get Oracle user name

util.get_user()

# Prompt for password for Oracle user name
    
password=getpass.getpass('Enter password for '+util.my_oracle_user+': ')

# Save encryption key

util.save_key()

# Save encrypted password

util.save_oracle_password(password)

