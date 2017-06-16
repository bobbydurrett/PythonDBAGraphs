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

simplesqlstat.py

Execution statistics for one SQL statement

"""

import myplot
import util

def simplesqlstat(sql_id):
    q_string = """
select 
sn.END_INTERVAL_TIME,
ss.executions_delta,
ELAPSED_TIME_DELTA/(executions_delta*1000) ELAPSED_AVG_MS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.sql_id = '""" 
    q_string += sql_id
    q_string += """'
and ss.snap_id=sn.snap_id
and executions_delta > 0
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
order by ss.snap_id,ss.sql_id"""
    return q_string

database,dbconnection = util.script_startup('Run statistics for one SQL id')

# Get user input

sql_id=util.input_with_default('SQL_ID','acrg0q0qtx3gr')

q = simplesqlstat(sql_id);

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "Sql_id "+sql_id+" on "+database+" database"
myplot.ylabel1 = "Number of executions"
myplot.ylabel2 = "Averaged Elapsed Milliseconds"

util.exit_no_results(r)

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()