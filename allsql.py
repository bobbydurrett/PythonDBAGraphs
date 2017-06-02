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

allsql.py

Execution statistics for all SQL statements

"""

import myplot
import util

def allsql():
    q_string = """select 
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
sum(ss.executions_delta) TOTAL_EXECUTIONS,
to_char(sum(ELAPSED_TIME_DELTA)/(sum(executions_delta)*1000)) ELAPSED_AVG_MS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where 
ss.snap_id=sn.snap_id
and executions_delta > 0
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME"""
    return q_string

database,dbconnection = util.script_startup('Run statistics for all sql statements')

# Build and run query

q = allsql();

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "All SQL statements on "+database+" database"
myplot.ylabel1 = "Number of executions"
myplot.ylabel2 = "Averaged Elapsed Milliseconds"

myplot.xlabels = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()
