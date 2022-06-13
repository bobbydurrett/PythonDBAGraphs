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

activeshared.py

Average number of active shared server connections

"""

import myplot
import util

def activeshared(start_time,end_time,instance_number):
    q_string = """select 
sn.END_INTERVAL_TIME,
(after.SAMPLED_ACTIVE_CONN-before.SAMPLED_ACTIVE_CONN)/(after.NUM_SAMPLES - before.NUM_SAMPLES) average_active
from 
DBA_HIST_SHARED_SERVER_SUMMARY before,
DBA_HIST_SHARED_SERVER_SUMMARY after,
DBA_HIST_SNAPSHOT sn
where 
before.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """
 and
before.INSTANCE_NUMBER = sn.INSTANCE_NUMBER and
before.INSTANCE_NUMBER = after.INSTANCE_NUMBER and
before.SNAP_ID = sn.SNAP_ID and
before.SNAP_ID + 1 = after.SNAP_ID and
before.DBID = sn.DBID and
before.DBID = after.DBID and
after.NUM_SAMPLES > before.NUM_SAMPLES and
after.SAMPLED_ACTIVE_CONN >= before.SAMPLED_ACTIVE_CONN and
END_INTERVAL_TIME 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
order by sn.SNAP_ID"""
    return q_string

database,dbconnection = util.script_startup('Active shared server connections')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')

# Build and run query

q = activeshared(start_time,end_time,instance_number);

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "Active shared server connections on "+database+" database, instance "+instance_number
myplot.ylabel1 = "Number of active sessions"

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line()
