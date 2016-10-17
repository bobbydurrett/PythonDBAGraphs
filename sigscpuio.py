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

sigscpuio.py

Plots elapsed, cpu, and io for a group of sql statements based
on their signatures.  

"""

import myplot
import util
import signatures

database,dbconnection = util.script_startup('SQL statments by signature CPU and IO')

queryobj = signatures.groupofsignatures()

lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

for line in lines:
    if len(line) > 0:
        queryobj.add_signature(int(line))

querytext = queryobj.build_query2()

results = dbconnection.run_return_flipped_results(querytext)

if results == None:
    print "No results returned"
    exit

# plot query

myplot.xlabels = results[0]
myplot.ylists = results[1:]
    
myplot.title = "SQL matching group of signatures on "+database+" database elapsed CPU IO"
myplot.ylabel1 = "Seconds"
    
myplot.ylistlabels=["Elapsed","CPU+IO","IO"]

myplot.line()
