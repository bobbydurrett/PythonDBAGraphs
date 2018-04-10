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

sqlstatcpuio.py

Plots total elapsed, cpu, and io seconds for a single sql_id.

"""

import myplot
import util

def sqlstatcpuio(sql_id,start_time,end_time):
    q_string = """
select
sn.END_INTERVAL_TIME,
sum(ELAPSED_TIME_DELTA)/1000000 ELAPSED_SECONDS,
(sum(CPU_TIME_DELTA)+sum(IOWAIT_DELTA))/1000000 CPU_IO_SECONDS,
sum(IOWAIT_DELTA)/1000000 IO_SECONDS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.snap_id=sn.snap_id
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
and ss.SQL_ID='""" 
    q_string += sql_id
    q_string += """' and
END_INTERVAL_TIME 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME
"""
    return q_string

database,dbconnection = util.script_startup('Elapsed, CPU, and IO for one SQL id')

sql_id=util.input_with_default('SQL_ID','acrg0q0qtx3gr')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

querytext = sqlstatcpuio(sql_id,start_time,end_time)

results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "Sql_id "+sql_id+" on "+database+" database"
myplot.ylabel1 = "Seconds"
    
myplot.ylistlabels=["Elapsed","CPU+IO","IO"]

myplot.line()
