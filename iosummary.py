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

iosummary.py

Graph i/o metrics for overall database.

"""

import myplot
import util

def iosummary(start_time,end_time):
    q_string = """
select 
sn.END_INTERVAL_TIME,
sum((after.PHYBLKRD - before.PHYBLKRD)*after.BLOCK_SIZE)/(1024*1024*1024*1024),
sum((after.PHYBLKWRT - before.PHYBLKWRT)*after.BLOCK_SIZE)/(1024*1024*1024*1024),
trunc(10*sum(after.READTIM-before.READTIM)/
sum(1+after.PHYRDS+-before.PHYRDS)),
trunc(10*sum(after.WRITETIM-before.WRITETIM)/
sum(1+after.PHYWRTS+-before.PHYWRTS))
from DBA_HIST_FILESTATXS before, DBA_HIST_FILESTATXS after,DBA_HIST_SNAPSHOT sn
where 
after.file#=before.file# and
after.snap_id=before.snap_id+1 and
before.instance_number=after.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
after.PHYBLKRD >= before.PHYBLKRD and
after.PHYBLKWRT >= before.PHYBLKWRT and
after.READTIM >= before.READTIM and
after.WRITETIM >= before.WRITETIM and
after.PHYRDS >= before.PHYRDS and
after.PHYWRTS >= before.PHYWRTS and
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

database,dbconnection = util.script_startup('I/O Summary')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

query = iosummary(start_time,end_time)

results = dbconnection.run_return_flipped_results(query)

util.exit_no_results(results)

date_times = results[0]
terabytes_read = results[1]
terabytes_written = results[2]
ave_read_time_milliseconds = results[3]
ave_write_time_milliseconds = results[4]
num_rows = len(date_times)
            
# plot query
    
myplot.xdatetimes = date_times
myplot.ylists = [terabytes_read,terabytes_written,ave_read_time_milliseconds,ave_write_time_milliseconds]

myplot.title = "IO summary for "+database+" database"
myplot.ylabel1 = "Terabytes read"
myplot.ylabel2 = "Terabytes written"
myplot.ylabel3 = "Average read time in milliseconds"
myplot.ylabel4 = "Average write time in milliseconds"

myplot.ylistlabels=["Terabytes read","Terabytes written","Average read time in milliseconds", \
"Average write time in milliseconds"]

myplot.line_4subplots()
