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

sessioncounts.py

Graph connected session count

"""

import myplot
import util

def sessioncounts(start_time,end_time,instance_number):
    q_string = """select 
snap.END_INTERVAL_TIME,
stat.value session_count
from
DBA_HIST_SYSSTAT stat,
DBA_HIST_SNAPSHOT snap
where
stat.SNAP_ID = snap.SNAP_ID and
stat.DBID = snap.DBID and
stat.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """ and
stat.INSTANCE_NUMBER = snap.INSTANCE_NUMBER and
stat.STAT_NAME = 'logons current' and
snap.END_INTERVAL_TIME 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
order by 
snap.END_INTERVAL_TIME"""
    return q_string

database,dbconnection = util.script_startup('Graph connected session count')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')

query = sessioncounts(start_time,end_time,instance_number)

results = dbconnection.run_return_flipped_results(query)

util.exit_no_results(results)

date_times = results[0]
session_counts = results[1]
num_rows = len(date_times)
            
# plot query
    
myplot.xdatetimes = date_times
myplot.ylists = [session_counts]

myplot.title = "Number of connected sessions on "+database+" database, instance "+instance_number
myplot.ylabel1 = "Number of sessions"
    
myplot.ylistlabels=["logons current"]

myplot.line()
