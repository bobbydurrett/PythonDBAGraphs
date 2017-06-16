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

query = """
select 
snap.END_INTERVAL_TIME,
stat.value session_count
from
DBA_HIST_SYSSTAT stat,
DBA_HIST_SNAPSHOT snap
where
stat.SNAP_ID = snap.SNAP_ID and
stat.DBID = snap.DBID and
stat.INSTANCE_NUMBER = snap.INSTANCE_NUMBER and
stat.STAT_NAME = 'logons current'
order by 
snap.END_INTERVAL_TIME
"""

database,dbconnection = util.script_startup('Graph connected session count')

results = dbconnection.run_return_flipped_results(query)

util.exit_no_results(results)

date_times = results[0]
session_counts = results[1]
num_rows = len(date_times)
            
# plot query
    
myplot.xdatetimes = date_times
myplot.ylists = [session_counts]

myplot.title = "Number of connected sessions on "+database+" database"
myplot.ylabel1 = "Number of sessions"
    
myplot.ylistlabels=["logons current"]

myplot.line()
