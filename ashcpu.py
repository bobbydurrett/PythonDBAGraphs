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

ashcpu.py

Generates a graph that shows cpu usage within an Oracle database
by various parts of the application. The graph is configured by lines in 
the text file ashcpufile.txt.

Each line is part of a client machine name and a label
for machines with that pattern.

For example:

abcd WEBFARM

Any client machines with the string abcd in their name 
will have their database cpu usage grouped into the category WEBFARM.

The graph is hard coded to only look at CPU usage between 8 am and 5 pm
of the day of the week specified. This is intended to look at CPU usage
during the work day.

"""

import saveawr
import perfq
import myplot
import util

database,dbconnection = util.script_startup('Database CPU by Application Area')

day=raw_input('Enter day of week: ')
    
user=util.my_oracle_user
 
c = perfq.cpubymachine(day,8,17)
    
lines = util.read_config_file(util.config_dir,database+util.ashcpu_file)

for l in lines:
    args = l.split()
    if len(args) == 2:
        c.add_machine(args[0],args[1])
    
querytext = c.build_query()
    
h = saveawr.day_history(dbconnection,day,'ASHCPUBYMACHINE',querytext)
    
results = h.save_day_results()
    
column_names = h.get_column_names()
    
# Load global variables for graph    

# Build list of labels for the bars
           
myplot.xlabels = []
for r in results:
    myplot.xlabels.append(r[0])
        
# Build a list of lists of y values
# and a list of the labels for each y value

myplot.ylists =  []
myplot.ylistlabels = []
    
for i in range(1,len(column_names)):
    yl=[]
    for r in results:
        val = 100.0 * myplot.nonetozero(r[i])
        yl.append(val)
    myplot.ylists.append(yl)
    myplot.ylistlabels.append(column_names[i])

# Misc labels and names

myplot.title = database.upper()+' CPU Working Hours '+day.capitalize()+'s'
myplot.ylabel1 = 'CPU % Utilization'
myplot.yticksuffix = '%'
myplot.filename = day.lower()+'.png'

# Run stacked bar graph
    
myplot.stacked_bar()
