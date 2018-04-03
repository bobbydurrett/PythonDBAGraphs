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

import myplot
import util
        
def onewait(wait_event,minimum_waits,start_time,end_time):
    q_string = """
select 
sn.END_INTERVAL_TIME,
(after.total_waits-before.total_waits) NUMBER_OF_WAITS,
(after.time_waited_micro-before.time_waited_micro)/(after.total_waits-before.total_waits) AVG_MICROSECONDS
from DBA_HIST_SYSTEM_EVENT before, DBA_HIST_SYSTEM_EVENT after,DBA_HIST_SNAPSHOT sn
where before.event_name='""" 
    q_string += wait_event
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
and 
after.event_name=before.event_name and
after.snap_id=before.snap_id+1 and
after.instance_number=1 and
before.instance_number=after.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
(after.total_waits-before.total_waits) > """
    q_string += str(minimum_waits)
    q_string += """
order by after.snap_id
"""
    return q_string

database,dbconnection = util.script_startup('One wait event')

# Get user input

wait_event=util.input_with_default('wait event','db file sequential read')

min_waits=int(util.input_with_default('minimum number of waits per hour','0'))

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

# Build and run query

q = onewait(wait_event,min_waits,start_time,end_time);

r = dbconnection.run_return_flipped_results(q)

# plot query
    
myplot.title = "'"+wait_event+"' waits on "+database+" database, minimum waits="+str(min_waits)
myplot.ylabel1 = "Number of events"
myplot.ylabel2 = "Averaged Elapsed Microseconds"

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()