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

def dbaashcount(start_time,end_time):
    """
    Group by minute.
    10 second samples.
    dba table
    """
    q_string = """
create table dbaashcount as
select
substr(to_char(all_time.sample_time,'YY/MM/DD HH24:MI'),4) date_minute,
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
group by to_char(all_time.sample_time,'YY/MM/DD HH24:MI')
"""
    return q_string
    
def vdollarashcount(start_time,end_time):
    """
    Group by minute.
    10 second samples.
    v$ table
    """
    q_string = """
create table combinedashcount as
select
substr(to_char(all_time.sample_time,'YY/MM/DD HH24:MI'),4) date_minute,
sum(all_time.cnt)/60 all_count,
sum(nvl(cpu_time.cnt,0))/60 cpu_count
from
(select 
sample_time,
count(*) cnt
from V$ACTIVE_SESSION_HISTORY a
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
from V$ACTIVE_SESSION_HISTORY a
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
group by to_char(all_time.sample_time,'YY/MM/DD HH24:MI')
"""
    return q_string

database,dbconnection = util.script_startup('ASH active session counts')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

# first get ash counts by minutes from dba view

dbconnection.run_return_no_results_catch_error("drop table dbaashcount")
 
dbacrtable = dbaashcount(start_time,end_time)

dbconnection.run_return_no_results(dbacrtable);

# now get from ash view put in combined table first

dbconnection.run_return_no_results_catch_error("drop table combinedashcount")

vdcrtable = vdollarashcount(start_time,end_time)

dbconnection.run_return_no_results(vdcrtable)

# insert dba rows for date and minute not in v$

insert_sql = """
insert into combinedashcount
select * from dbaashcount d
where d.date_minute not in
(select date_minute from combinedashcount)"""

dbconnection.run_return_no_results(insert_sql)

dbconnection.commit()

querytext = """
select * from combinedashcount
order by date_minute"""
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xlabels = results[0]
myplot.ylists = results[1:]
    
myplot.title = "ASH active session count for "+database+" database"
myplot.ylabel1 = "Sessions"
    
myplot.ylistlabels=["Total","CPU"]

myplot.line()