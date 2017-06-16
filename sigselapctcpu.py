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

sigselapctcpu.py

Plots elapsed for a group of sql statements based
on their signatures against percent CPU of the host. 

"""

import myplot
import util
import signatures

database,dbconnection = util.script_startup('SQL statments by signature Elapsed and CPU')

queryobj = signatures.groupofsignatures()

lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

for line in lines:
    if len(line) > 0:
        queryobj.add_signature(int(line))

querytext = queryobj.build_query3()

results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "SQL matching group of signatures on "+database+" database elapsed versus cpu"
myplot.ylabel1 = "Minutes versus Percentage"
    
myplot.ylistlabels=["CPU % Busy","Elapsed in Minutes"]

myplot.line()
