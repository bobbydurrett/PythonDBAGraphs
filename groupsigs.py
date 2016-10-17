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

groupsigs.py

This shows the average elapsed time and total number of executions for 
a group of SQL statements defined by their force matching signature.
A signature represents a group of queries that are the same except for their
constants. The goal of this query is to pick some group of queries 
that we care about such as the main queries the users use every day and
show their performance over time. It does hide the details of the individual
queries but may have value if we choose the best set of signatures.   


"""

import perfq
import myplot
import util

database,dbconnection = util.script_startup('Stats for SQL statments by signature')

queryobj = perfq.groupofsignatures()

lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

for line in lines:
    if len(line) > 0:
        queryobj.add_signature(int(line))

querytext = queryobj.build_query()

results = dbconnection.run_return_flipped_results(querytext)

if results == None:
    print "No results returned"
    exit

# plot query
    
myplot.title = "SQL matching group of signatures on "+database+" database elapsed versus executions"
myplot.ylabel1 = "Number of executions"
myplot.ylabel2 = "Averaged Elapsed Microseconds"

myplot.xlabels = results[0]
myplot.ylists = results[1:]

myplot.line_2subplots()
