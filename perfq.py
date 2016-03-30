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

perfq.py

This package contains code to build queries that are used 
in Oracle database performance tuning.

"""

class cpubymachine():
    def __init__(self,day,start_hour,stop_hour):
        self.day = day.upper()
        self.start_hour = start_hour
        self.stop_hour = stop_hour
        self.labels = []
        self.machines = []
         
    def add_machine(self,machine,label):
        if label not in self.labels:
            self.labels.append(label)
        self.machines.append([label,machine.upper()])
        
    def build_case(self):
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
        st_string = "to_char(SAMPLE_TIME,'DAY')='"+self.day
        for i in range(9-len(self.day)):
           st_string += " "
        st_string += "' and\n"
        st_string += "to_number(to_char(SAMPLE_TIME,'HH24')) between "
        st_string += str(self.start_hour)+" and "+str(self.stop_hour)+" and\n"
        return st_string
        
    def build_query(self):
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
        
class onewait():
    def __init__(self,wait_event,mimimum_waits):
        self.wait_event = wait_event
        self.mimimum_waits = mimimum_waits
        
    def build_query(self):
        q_string = """
select to_char(sn.END_INTERVAL_TIME,'YYYY-MM-DD HH24:MI') DATE_TIME,
(after.total_waits-before.total_waits) NUMBER_OF_WAITS,
(after.time_waited_micro-before.time_waited_micro)/(after.total_waits-before.total_waits) AVG_MICROSECONDS
from DBA_HIST_SYSTEM_EVENT before, DBA_HIST_SYSTEM_EVENT after,DBA_HIST_SNAPSHOT sn
where before.event_name='""" 
        q_string += self.wait_event
        q_string += """' and
after.event_name=before.event_name and
after.snap_id=before.snap_id+1 and
after.instance_number=1 and
before.instance_number=after.instance_number and
after.snap_id=sn.snap_id and
after.instance_number=sn.instance_number and
(after.total_waits-before.total_waits) > """
        q_string += str(self.mimimum_waits)
        q_string += """
order by after.snap_id
"""
        return q_string
                         