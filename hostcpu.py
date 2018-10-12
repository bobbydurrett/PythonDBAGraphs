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

hostcpu.py

Shows the host level CPU percent used and load over time. 

"""

import myplot
import util

def myoscpu(instance_number):
    """
    Create myoscpu table with CPU data for selected instance.
    """
    q_string = """
create table myoscpu as
select
busy_v.SNAP_ID,
busy_v.VALUE BUSY_TIME,
idle_v.VALUE IDLE_TIME,
load_v.VALUE LOAD
from 
DBA_HIST_OSSTAT busy_v,
DBA_HIST_OSSTAT idle_v,
DBA_HIST_OSSTAT load_v
where
busy_v.SNAP_ID = idle_v.SNAP_ID AND
busy_v.DBID = idle_v.DBID AND
busy_v.INSTANCE_NUMBER = idle_v.INSTANCE_NUMBER AND
load_v.SNAP_ID = idle_v.SNAP_ID AND
load_v.DBID = idle_v.DBID AND
load_v.INSTANCE_NUMBER = idle_v.INSTANCE_NUMBER AND
busy_v.STAT_NAME = 'BUSY_TIME' AND
idle_v.STAT_NAME = 'IDLE_TIME' AND
load_v.STAT_NAME = 'LOAD' AND
busy_v.INSTANCE_NUMBER = """
    q_string += instance_number

    return q_string
    
def cpuquery(start_time,end_time):
    """
    Final query showing host cpu percent busy and load
    for the given date time range.
    """
    q_string = """
select 
sn.END_INTERVAL_TIME,
(100*BUSY_TIME)/(BUSY_TIME+IDLE_TIME),
LOAD HOST_CPU_LOAD
from 
myoscpudiff my,
DBA_HIST_SNAPSHOT sn
where 
my.SNAP_ID = sn.SNAP_ID AND
sn.END_INTERVAL_TIME between
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
order by my.SNAP_ID
    """
    return q_string

database,dbconnection = util.script_startup('Host CPU')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')

# Get cpu busy, idle, and load for the selected instance

dbconnection.run_return_no_results_catch_error("drop table myoscpu")
 
crmyoscpu = myoscpu(instance_number)

dbconnection.run_return_no_results(crmyoscpu);

# now get the difference in cumulative cpu times between two snapshots

dbconnection.run_return_no_results_catch_error("drop table myoscpudiff")

crmyoscpudiff = """
create table myoscpudiff as
select
after.SNAP_ID,
(after.BUSY_TIME - before.BUSY_TIME) BUSY_TIME,
(after.IDLE_TIME - before.IDLE_TIME) IDLE_TIME,
after.LOAD 
from 
myoscpu before,
myoscpu after
where before.SNAP_ID + 1 = after.SNAP_ID"""

dbconnection.run_return_no_results(crmyoscpudiff)


querytext = cpuquery(start_time,end_time)
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "Host CPU for "+database+" database, instance "+instance_number
myplot.ylabel1 = "CPU"
    
myplot.ylistlabels=["Percent busy","Load"]

myplot.line()
