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

Graph of one wait event using ASH V$ table

"""

import myplot
import util

def dbaashcount(start_time,end_time,wait_event):
    """
    Group by minute.
    10 second samples.
    dba table
    """
    q_string = """
create table dbaashcount as
select
to_char(sample_time,'YYYY/MM/DD HH24:MI') date_minute,
count(*)/6 wait_count
from DBA_HIST_ACTIVE_SESS_HISTORY
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
and
event='""" 
    q_string += wait_event
    q_string += """'
group by to_char(sample_time,'YYYY/MM/DD HH24:MI')
"""
    return q_string
        
def vdollarashcount(start_time,end_time,wait_event):
    """
    Group by minute.
    1 second samples.
    v$ table
    """
    q_string = """
create table combinedashcount as
select
to_char(sample_time,'YYYY/MM/DD HH24:MI') date_minute,
count(*)/60 wait_count
from V$ACTIVE_SESSION_HISTORY
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
and
event='""" 
    q_string += wait_event
    q_string += """'
group by to_char(sample_time,'YYYY/MM/DD HH24:MI')
"""
    return q_string

database,dbconnection = util.script_startup('ASH one wait event')

# Get user input

wait_event=util.input_with_default('wait event','db file sequential read')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

# first get ash counts by minutes from dba view

dbconnection.run_return_no_results_catch_error("drop table dbaashcount")
 
dbacrtable = dbaashcount(start_time,end_time,wait_event)

dbconnection.run_return_no_results(dbacrtable);

# now get from ash view put in combined table first

dbconnection.run_return_no_results_catch_error("drop table combinedashcount")

vdcrtable = vdollarashcount(start_time,end_time,wait_event)

dbconnection.run_return_no_results(vdcrtable)

# insert dba rows for date and minute not in v$

insert_sql = """
insert into combinedashcount
select * from dbaashcount d
where d.date_minute not in
(select date_minute from combinedashcount)"""

dbconnection.run_return_no_results(insert_sql)

dbconnection.commit()

# query final results grouped by minute

querytext = """
select
to_date(DATE_MINUTE,'YYYY/MM/DD HH24:MI'),
wait_count
from combinedashcount
order by date_minute"""
    
r = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(r)

# plot query
    
myplot.title = "Sessions waiting on '"+wait_event+"' waits on "+database+" database"
myplot.ylabel1 = "Number of sessions"

myplot.xdatetimes = r[0]
myplot.ylists = r[1:]

myplot.line()
