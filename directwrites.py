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

directwrites.py

Shows direct write I/O in time period. 

"""

import myplot
import util

def directwrites(start_time,end_time,instance_number):
    """
    Direct write activity by snapshot
    """
    q_string = """
select 
sn.END_INTERVAL_TIME,
after.SMALL_WRITE_MEGABYTES+after.LARGE_WRITE_MEGABYTES-before.SMALL_WRITE_MEGABYTES-before.LARGE_WRITE_MEGABYTES
from DBA_HIST_IOSTAT_FUNCTION before, DBA_HIST_IOSTAT_FUNCTION after,DBA_HIST_SNAPSHOT sn
where 
after.snap_id=before.snap_id+1 and
before.instance_number=after.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
after.FUNCTION_NAME = 'Direct Writes' and
before.FUNCTION_NAME = after.FUNCTION_NAME and
sn.END_INTERVAL_TIME 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and after.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """
order by sn.END_INTERVAL_TIME
"""
    return q_string

database,dbconnection = util.script_startup('Direct Write IO')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')
 
querytext = directwrites(start_time,end_time,instance_number)
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "Direct Write IO for "+database+" database, instance "+instance_number
myplot.ylabel1 = "Megabytes"
    
myplot.ylistlabels=["Direct Writes"]

myplot.line()
