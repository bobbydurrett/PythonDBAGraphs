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

onewait.py

Graph of one wait event

"""

import perfq
import myplot
import util

database,dbconnection = util.script_startup('One wait event')

# Get user input

wait_event=util.input_with_default('wait event','db file sequential read')
min_waits=int(util.input_with_default('minimum number of waits per hour','0'))

# Build and run query

q = perfq.onewait(wait_event,min_waits);

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "'"+wait_event+"' waits on "+database+" database, minimum waits="+str(min_waits)
myplot.ylabel1 = "Number of events"
myplot.ylabel2 = "Averaged Elapsed Microseconds"

myplot.xlabels = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()