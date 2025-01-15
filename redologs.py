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

redologs.py

Shows the number of archived redo logs per hour.

"""

import myplot
import util
    
def redoquery(start_time,end_time):
    """
    Query showing number of redo logs per hour
    """
    q_string = """
select
to_date(date_hour,'YYYY-MM-DD HH24'),
num_logs
from
(select 
to_char(FIRST_TIME,'YYYY-MM-DD HH24') date_hour,
count(*) num_logs
from 
v$archived_log
where 
FIRST_TIME between
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
group by 
to_char(FIRST_TIME,'YYYY-MM-DD HH24') 
order by 
to_char(FIRST_TIME,'YYYY-MM-DD HH24'))
    """
    return q_string

database,dbconnection = util.script_startup('Number of redo logs')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

querytext = redoquery(start_time,end_time)
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "Number of archived redo logs for "+database+" database"
myplot.ylabel1 = "Archived redo logs"
    
myplot.ylistlabels=["Number of logs"]

myplot.line()
