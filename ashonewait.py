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

Graph of one wait event using ASH V$ table

"""

import myplot
import util
        
def ashonewait(wait_event):
    q_string = """
select 
sample_time,
count(*) active_sessions
from V$ACTIVE_SESSION_HISTORY a
where 
event='""" 
    q_string += wait_event
    q_string += """'
group by sample_time
order by sample_time
"""
    return q_string

database,dbconnection = util.script_startup('ASH one wait event')

# Get user input

wait_event=util.input_with_default('wait event','db file sequential read')

# Build and run query

q = ashonewait(wait_event);

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "Sessions waiting on '"+wait_event+"' waits on "+database+" database"
myplot.ylabel1 = "Number of sessions"

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line()
