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

onesysstat.py

Shows the difference in one system statistic per snapshot
for a given time period.

"""

import myplot
import util

def onesysstat(start_time,end_time,instance_number,stat_name):
    """
    Build query for given statistic name stat_name.
    """
    q_string = """
select
sn.END_INTERVAL_TIME,
after.value-before.value value_difference
from 
DBA_HIST_SYSSTAT before,
DBA_HIST_SYSSTAT after,
DBA_HIST_SNAPSHOT sn
where 
before.STAT_NAME = '"""
    q_string += stat_name
    q_string += """' and
before.STAT_NAME = after.STAT_NAME and
before.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """ and
before.INSTANCE_NUMBER = sn.INSTANCE_NUMBER and
before.INSTANCE_NUMBER = after.INSTANCE_NUMBER and
before.SNAP_ID = sn.SNAP_ID and
before.SNAP_ID + 1 = after.SNAP_ID and
before.DBID = sn.DBID and
before.DBID = after.DBID and
after.value >= before.value and
sn.END_INTERVAL_TIME
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

database,dbconnection = util.script_startup('One System Statistic')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2018 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')

stat_name=util.input_with_default('System Statistic','bytes received via SQL*Net from client')

# Get and run query for one system statistic
 
querytext = onesysstat(start_time,end_time,instance_number,stat_name)
  
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "System statistic difference for "+database+" database, instance "+instance_number
myplot.ylabel1 = "Statistic value difference per snapshot"
    
myplot.ylistlabels=[stat_name]

myplot.line()
