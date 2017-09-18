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

show_saved.py

Restores saved data and displays graph.

"""

import myplot
import util

# Get full path to the .txt file that was saved when the graph was produced

file_name = util.input_no_default('Enter name of data file to be restored: ')

# Restore data into all of the myplot module global variables that are used
# by the different graphs

plot_name = myplot.restore_data(file_name) 

# Call the graphing routine that was used for this plot

if plot_name == 'stacked_bar':
    myplot.stacked_bar()
elif plot_name == 'line':
    myplot.line()
elif plot_name == 'line_2subplots':
    myplot.line_2subplots()
elif plot_name == 'line_4subplots':
    myplot.line_4subplots()
else:
    print('Invalid plot_name = '+plot_name)