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

space.py

Shows the growth in tablespace usage and allocation over time.

"""

import myplot
import util

def spaceq(start_time,end_time):
    """
    Build query for given statistic name stat_name.
    """
    q_string = """
select 
snap.END_INTERVAL_TIME,
sum(tsu.TABLESPACE_SIZE*dt.BLOCK_SIZE)/(1024*1024*1024) total_gigabytes,
sum(tsu.TABLESPACE_USEDSIZE*dt.BLOCK_SIZE)/(1024*1024*1024) used_gigabytes
from
DBA_HIST_TBSPC_SPACE_USAGE tsu,
DBA_HIST_SNAPSHOT snap,
V$TABLESPACE vt,
DBA_TABLESPACES dt
where
tsu.SNAP_ID = snap.SNAP_ID and
tsu.DBID = snap.DBID and
snap.instance_number = 1 and
tsu.TABLESPACE_ID = vt.TS# and
vt.NAME = dt.TABLESPACE_NAME and
snap.END_INTERVAL_TIME
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
group by snap.END_INTERVAL_TIME
order by snap.END_INTERVAL_TIME"""
    
    return q_string

database,dbconnection = util.script_startup('Tablespace usage')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2018 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

# Get and run query for one system statistic
 
querytext = spaceq(start_time,end_time)
  
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "Tablespace usage for "+database+" database"
myplot.ylabel1 = "Gigabytes"
    
myplot.ylistlabels=["Allocated","Used"]

myplot.line()
