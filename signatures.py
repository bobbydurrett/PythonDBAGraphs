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

signatures.py

This class is shared by several scripts that pull a list of 
signatures from a text file to include in a query.

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
sn.END_INTERVAL_TIME,
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
        
        For example:
            
select
sn.END_INTERVAL_TIME,
sum(ELAPSED_TIME_DELTA)/1000000 ELAPSED_SECONDS,
(sum(CPU_TIME_DELTA)+sum(IOWAIT_DELTA))/1000000 CPU_IO_SECONDS,
sum(IOWAIT_DELTA)/1000000 IO_SECONDS
from DBA_HIST_SQLSTAT ss,DBA_HIST_SNAPSHOT sn
where ss.snap_id=sn.snap_id
and ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
and ss.FORCE_MATCHING_SIGNATURE in
(
14038313233049026256,
18385146879684525921,
11181311136166944889,
187803040686893225
)
group by sn.END_INTERVAL_TIME
order by sn.END_INTERVAL_TIME

        """
        q_string = """
select
sn.END_INTERVAL_TIME,
sum(ELAPSED_TIME_DELTA)/1000000 ELAPSED_SECONDS,
(sum(CPU_TIME_DELTA)+sum(IOWAIT_DELTA))/1000000 CPU_IO_SECONDS,
sum(IOWAIT_DELTA)/1000000 IO_SECONDS
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
    def build_query3(self):
        """ 
        Build query for use with single plot with 
        total elapsed versus percent busy cpu.
        
        For example:
            
select
sn.END_INTERVAL_TIME,
pb.percent_busy,
ela.ELAPSED_MINUTES
from
(select 
idle_before.SNAP_ID,
(100*(busy_after.value-busy_before.value)/
(busy_after.value-busy_before.value +
idle_after.value-idle_before.value)) percent_busy
from 
DBA_HIST_OSSTAT idle_before, 
DBA_HIST_OSSTAT idle_after, 
DBA_HIST_OSSTAT busy_before,
DBA_HIST_OSSTAT busy_after
where
idle_before.SNAP_ID=busy_before.SNAP_ID and
idle_after.SNAP_ID=busy_after.SNAP_ID and
idle_before.SNAP_ID+1=idle_after.SNAP_ID and
idle_before.STAT_NAME='IDLE_TIME' and
idle_after.STAT_NAME='IDLE_TIME' and
busy_before.STAT_NAME='BUSY_TIME' and
busy_after.STAT_NAME='BUSY_TIME') pb,
(select
SNAP_ID,
sum(ELAPSED_TIME_DELTA)/(60*1000000) ELAPSED_MINUTES
from DBA_HIST_SQLSTAT ss
where 
ss.FORCE_MATCHING_SIGNATURE in
(
14038313233049026256,
18385146879684525921,
11181311136166944889,
187803040686893225
)
group by SNAP_ID) ela,
DBA_HIST_SNAPSHOT sn
where 
pb.snap_id=ela.snap_id and
pb.snap_id=sn.snap_id
order by pb.snap_id

        """
        q_string = """
select
sn.END_INTERVAL_TIME,
pb.percent_busy,
ela.ELAPSED_MINUTES
from
(select 
idle_before.SNAP_ID,
(100*(busy_after.value-busy_before.value)/
(busy_after.value-busy_before.value +
idle_after.value-idle_before.value)) percent_busy
from 
DBA_HIST_OSSTAT idle_before, 
DBA_HIST_OSSTAT idle_after, 
DBA_HIST_OSSTAT busy_before,
DBA_HIST_OSSTAT busy_after
where
idle_before.SNAP_ID=busy_before.SNAP_ID and
idle_after.SNAP_ID=busy_after.SNAP_ID and
idle_before.SNAP_ID+1=idle_after.SNAP_ID and
idle_before.STAT_NAME='IDLE_TIME' and
idle_after.STAT_NAME='IDLE_TIME' and
busy_before.STAT_NAME='BUSY_TIME' and
busy_after.STAT_NAME='BUSY_TIME') pb,
(select
SNAP_ID,
sum(ELAPSED_TIME_DELTA)/(60*1000000) ELAPSED_MINUTES
from DBA_HIST_SQLSTAT ss
where 
ss.FORCE_MATCHING_SIGNATURE in
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
group by SNAP_ID) ela,
DBA_HIST_SNAPSHOT sn
where 
pb.snap_id=ela.snap_id and
pb.snap_id=sn.snap_id
order by pb.snap_id
"""        
        return q_string

    def build_query4(self):
        """ 
        Build query for use with single plot with 
        executions, average elapsed, cpu percent
        and average single block IO time.
        """
        q_string = """
select
sn.END_INTERVAL_TIME,
pb.percent_busy,
ela.EXECUTIONS_SCALED,
ela.ELAPSED_AVG,
rd.READ_AVG
from
(select 
idle_before.SNAP_ID,
(100*(busy_after.value-busy_before.value)/
(busy_after.value-busy_before.value +
idle_after.value-idle_before.value)) percent_busy
from 
DBA_HIST_OSSTAT idle_before, 
DBA_HIST_OSSTAT idle_after, 
DBA_HIST_OSSTAT busy_before,
DBA_HIST_OSSTAT busy_after
where
idle_before.SNAP_ID=busy_before.SNAP_ID and
idle_after.SNAP_ID=busy_after.SNAP_ID and
idle_before.SNAP_ID+1=idle_after.SNAP_ID and
idle_before.STAT_NAME='IDLE_TIME' and
idle_after.STAT_NAME='IDLE_TIME' and
busy_before.STAT_NAME='BUSY_TIME' and
busy_after.STAT_NAME='BUSY_TIME') pb,
(select
SNAP_ID,
sum(ss.executions_delta)/100000 EXECUTIONS_SCALED,
sum(ELAPSED_TIME_DELTA)/((sum(executions_delta)+1)) ELAPSED_AVG
from DBA_HIST_SQLSTAT ss
where 
ss.FORCE_MATCHING_SIGNATURE in
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
group by SNAP_ID) ela,
(
select before.snap_id,
(after.time_waited_micro-before.time_waited_micro)/(1000*(after.total_waits-before.total_waits)) READ_AVG
from DBA_HIST_SYSTEM_EVENT before, DBA_HIST_SYSTEM_EVENT after
where before.event_name='db file sequential read' and
after.event_name=before.event_name and
after.snap_id=before.snap_id+1 and
after.instance_number=1 and
before.instance_number=after.instance_number and
(after.total_waits-before.total_waits) > 0
) rd,
DBA_HIST_SNAPSHOT sn
where 
pb.snap_id=ela.snap_id and
pb.snap_id=rd.snap_id and
pb.snap_id=sn.snap_id
order by pb.snap_id
"""        
        return q_string
