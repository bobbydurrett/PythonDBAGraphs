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

perfq.py

This package contains code to build queries that are used 
in Oracle database performance tuning.

"""

"""
Example of the type of query that this class builds:

select * from 
(
select
CASE 
WHEN  UPPER(MACHINE) like '%webhost%'  THEN 'WEBFARM'
WHEN  UPPER(MACHINE) like '%mobhost%'  THEN 'MOBILE'
ELSE 'OTHER' END labels,
to_char(sample_time,'YYYY-MM-DD') WEDNESDAY_DATE,
(count(*)*10)/(10*3600*12) percent_cpu
from DBA_HIST_ACTIVE_SESS_HISTORY
where
to_char(SAMPLE_TIME,'DAY')='WEDNESDAY' and
to_number(to_char(SAMPLE_TIME,'HH24')) between 8 and 17 and
SESSION_STATE='ON CPU'
group by 
CASE 
WHEN  UPPER(MACHINE) like '%webhost%'  THEN 'WEBFARM'
WHEN  UPPER(MACHINE) like '%mobhost%'  THEN 'MOBILE'
ELSE 'OTHER' END,
to_char(sample_time,'YYYY-MM-DD')
)
pivot
(
sum(percent_cpu)
for labels in (
'WEBFARM',
'MOBILE',
'OTHER'
)) order by WEDNESDAY_DATE

This summarizes the CPU usage on the database on Wednesdays during
working hours grouping by machine names. It shows which group of 
database clients are consuming the most database cpu resources.

"""

class cpubymachine():
    def __init__(self,day,start_hour,stop_hour):
        self.day = day.upper()
        self.start_hour = start_hour
        self.stop_hour = stop_hour
        self.labels = []
        self.machines = []
         
    def add_machine(self,machine,label):
        """ 
        Record a relationship between a machine name and
        a meaningful label of your choice. I.e. machine=webhost
        label=WEBFARM. Let's you choose a readable label for a 
        group of machines. There is a many to one relationship 
        between machine and label. So you can call this multiple
        times with the same label and all client host machines that 
        match and of the machine names will have their cpu consolidated
        under the label.
        """
        # labels has only one entry per label
        if label not in self.labels:
            self.labels.append(label)
        # machines has one entry per machine.
        # could have multiple entries for the same label
        self.machines.append([label,machine.upper()])
        
    def build_case(self):
        """
        This function builds this part of our example SQL statement:
CASE 
WHEN  UPPER(MACHINE) like '%webhost%'  THEN 'WEBFARM'
WHEN  UPPER(MACHINE) like '%mobhost%'  THEN 'MOBILE'
ELSE 'OTHER' END

        Does not show in my example but with multiple machines for a 
        label it builds an OR condition before the THEN keywords.

        """
        case_string = "CASE \n"
        for l in self.labels:
            case_string +=  "WHEN "
            first_machine = True
            for m in self.machines:
                if m[0] == l:
                    if not first_machine:
                       case_string +=  " OR "
                    else:
                       first_machine = False
                    case_string += " UPPER(MACHINE) like '%"+m[1]+"%' "
            case_string += " THEN '"+l+"'\n"
        case_string += "ELSE 'OTHER' END"
        return case_string
         
    def build_sample_time(self):
        """
        Builds this part of our example SQL:
            
to_char(SAMPLE_TIME,'DAY')='WEDNESDAY' and
to_number(to_char(SAMPLE_TIME,'HH24')) between 8 and 17 and

        Puts in the day of the week and start and stop time.

        """
        st_string = "to_char(SAMPLE_TIME,'DAY')='"+self.day
        for i in range(9-len(self.day)):
           st_string += " "
        st_string += "' and\n"
        st_string += "to_number(to_char(SAMPLE_TIME,'HH24')) between "
        st_string += str(self.start_hour)+" and "+str(self.stop_hour)+" and\n"
        return st_string
        
    def build_query(self):
        """ puts the query together"""
        q_string = """
select * from 
(
select
"""
        q_string += self.build_case()
        q_string += """ labels,
to_char(sample_time,'YYYY-MM-DD') """
        q_string += self.day+"_DATE,\n"
        q_string += """(count(*)*10)/(10*3600*12) percent_cpu
from DBA_HIST_ACTIVE_SESS_HISTORY
where
"""
        q_string += self.build_sample_time()
        q_string += """SESSION_STATE='ON CPU'
group by 
"""
        q_string += self.build_case()
        q_string += """,
to_char(sample_time,'YYYY-MM-DD')
)
pivot
(
sum(percent_cpu)
for labels in (
"""
        for l in self.labels:
             q_string += "'"+l+"',\n"
        q_string += "'OTHER'\n"
        q_string += ")) order by "+self.day+"_DATE"
        
        return q_string
        
def onewait(wait_event,minimum_waits):
    q_string = """
select to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
(after.total_waits-before.total_waits) NUMBER_OF_WAITS,
(after.time_waited_micro-before.time_waited_micro)/(after.total_waits-before.total_waits) AVG_MICROSECONDS
from DBA_HIST_SYSTEM_EVENT before, DBA_HIST_SYSTEM_EVENT after,DBA_HIST_SNAPSHOT sn
where before.event_name='""" 
    q_string += wait_event
    q_string += """' and
after.event_name=before.event_name and
after.snap_id=before.snap_id+1 and
after.instance_number=1 and
before.instance_number=after.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
(after.total_waits-before.total_waits) > """
    q_string += str(minimum_waits)
    q_string += """
order by after.snap_id
"""
    return q_string
        
def simplesqlstat(sql_id):
    q_string = """
select 
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
ss.executions_delta,
ELAPSED_TIME_DELTA/(executions_delta*1000) ELAPSED_AVG_MS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.sql_id = '""" 
    q_string += sql_id
    q_string += """'
and ss.snap_id=sn.snap_id
and executions_delta > 0
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
order by ss.snap_id,ss.sql_id"""
    return q_string
                         
def allsql():
    q_string = """select 
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
sum(ss.executions_delta) TOTAL_EXECUTIONS,
sum(ELAPSED_TIME_DELTA)/(sum(executions_delta)*1000) ELAPSED_AVG_MS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where 
ss.snap_id=sn.snap_id
and executions_delta > 0
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME"""
    return q_string
    
"""
Example of the type of query that this class builds:

select
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
sum(ss.executions_delta) TOTAL_EXECUTIONS,
sum(ELAPSED_TIME_DELTA)/((sum(executions_delta)+1)) ELAPSED_AVG_MICRO
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.snap_id=sn.snap_id
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
and ss.FORCE_MATCHING_SIGNATURE in
(
14038313233049026256,
18385146879684525921,
2974462313782736551,
12492389898598272683,
14164303807833460050,
15927676903549361476,
9120348263769454156,
10517599934976061598,
6987137087681155918,
11181311136166944889,
187803040686893225
)
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME;

This shows the average elapsed time and total number of executions for 
a group of SQL statements defined by their force matching signature.
A signature represents a group of queries that are the same except for their
constants. The goal of this query is to pick some group of queries 
that we care about such as the main queries the users use every day and
show their performance over time. It does hide the details of the individual
queries but may have value if we choose the best set of signatures.

"""

class groupofsignatures():
    def __init__(self):
        self.signatures = []
         
    def add_signature(self,signature):
        """ 
        Add to the list of FORCE_MATCHING_SIGNATURE values
        for the query.
        """
        # signatures has only one entry per signature
        if signature not in self.signatures:
            self.signatures.append(signature)
        
    def build_query(self):
        """ puts the query together"""
        q_string = """
select
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
sum(ss.executions_delta) TOTAL_EXECUTIONS,
sum(ELAPSED_TIME_DELTA)/((sum(executions_delta)+1)) ELAPSED_AVG_MICRO
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.snap_id=sn.snap_id
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
and ss.FORCE_MATCHING_SIGNATURE in
(
"""
        # Add the signatures to the query with commas
        # and newlines after all but the last one.
        snum = 0;
        slen = len(self.signatures)
        for s in self.signatures:
            q_string += str(s)
            snum += 1;
            if snum < slen:
                q_string += ",\n"             
        q_string += """
)
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME
"""        
        return q_string
        
    def build_query2(self):
        """ 
        Restructures query for use with single plot with 
        elapsed, cpu, and IO.
        """
        q1_string = self.build_query()
        q2_string = q1_string[0:64]
        q2_string += """
sum(ELAPSED_TIME_DELTA)/1000000 ELAPSED_SECONDS,
sum(CPU_TIME_DELTA)/1000000 CPU_SECONDS,
sum(IOWAIT_DELTA)/1000000 IO_SECONDS
"""
        q2_string += q1_string[178:]
        
        return q2_string
