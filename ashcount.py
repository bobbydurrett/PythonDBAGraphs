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

ashcount.py

Shows ASH active session counts in time period. 

"""

import myplot
import util

def ashcputotal(start_time,end_time):
    """
    Group by minute.
    10 second samples.
    """
    q_string = """
select
to_char(all_time.sample_time,'MM/DD HH24:MI'),
sum(all_time.cnt)/6 all_count,
sum(nvl(cpu_time.cnt,0))/6 cpu_count
from
(select 
sample_time,
count(*) cnt
from DBA_HIST_ACTIVE_SESS_HISTORY a
where 
sample_time 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
group by sample_time) all_time,
(select 
sample_time,
count(*) cnt
from DBA_HIST_ACTIVE_SESS_HISTORY a
where 
sample_time 
between 
to_date('"""
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS') and
session_state = 'ON CPU'
group by sample_time) cpu_time
where
all_time.sample_time=cpu_time.sample_time(+)
group by to_char(all_time.sample_time,'MM/DD HH24:MI')
order by to_char(all_time.sample_time,'MM/DD HH24:MI')
"""
    return q_string

database,dbconnection = util.script_startup('ASH active session counts')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')
 
querytext = ashcputotal(start_time,end_time)
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xlabels = results[0]
myplot.ylists = results[1:]
    
myplot.title = "ASH active session count for "+database+" database"
myplot.ylabel1 = "Sessions"
    
myplot.ylistlabels=["Total","CPU"]

myplot.line()