"""
PythonDBAGraphs: Graphs to help with Oracle Database Tuning
Copyright (C) 2020  Robert Taft Durrett (Bobby Durrett)

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

ashcpuprog.py

Generates a graph that shows cpu usage within an Oracle database
by various parts of the application. The graph is configured by lines in 
the text file DBNAMEashcpuprogfile.txt.

Each line is part of a client program name and a label
for programs with that pattern.

For example:

PSAESRV APPENGINE

Any client programs with the string PSAESRV in their name 
will have their database cpu usage grouped into the category APPENGINE.

The graph is hard coded to only look at CPU usage between 8 am and 5 pm
of the day of the week specified. This is intended to look at CPU usage
during the work day.

"""

import myplot
import util
import db

"""
Example of the type of query that cpubyprogram class builds:

select
MONDAY_DATE,
sum(case when LABELS ='BATCH' then percent_cpu else 0 end) BATCH,
sum(case when LABELS ='WEB' then percent_cpu else 0 end) WEB,
sum(case when LABELS ='REPORTING' then percent_cpu else 0 end) REPORTING,
sum(case when LABELS ='BACKUPS' then percent_cpu else 0 end) BACKUPS,
sum(case when LABELS ='OTHER' then percent_cpu else 0 end) OTHER
from
(
select
CASE
WHEN  UPPER(PROGRAM) like '%PSAESRV@%'  OR  UPPER(PROGRAM) like '%SQR%'  OR  UPPER(PROGRAM) like '%PSRUN%'  OR  UPPER(PROGRAM) like '%PSPRCSRV%'  OR  UPPER(PROGRAM) like '%PSMSTPRC%'  OR  UPPER(PROGRAM) like '%SQLPLUS%'  THEN 'BATCH'
WHEN  UPPER(PROGRAM) like '%PSAPPSRV%'  THEN 'WEB'
WHEN  UPPER(PROGRAM) like '%PSNVS%'  OR  UPPER(PROGRAM) like '%PSQRYSRV%'  OR  UPPER(PROGRAM) like '%PSAESRV.EXE%'  THEN 'REPORTING'
WHEN  UPPER(PROGRAM) like '%RMAN%'  THEN 'BACKUPS'
ELSE 'OTHER' END labels,
to_char(sample_time,'YYYY-MM-DD') MONDAY_DATE,
(count(*)*10)/(10*3600*12) percent_cpu
from DBA_HIST_ACTIVE_SESS_HISTORY
where
to_char(SAMPLE_TIME,'DAY')='MONDAY   ' and
to_number(to_char(SAMPLE_TIME,'HH24')) between 8 and 17 and
SESSION_STATE='ON CPU'
group by
CASE
WHEN  UPPER(PROGRAM) like '%PSAESRV@%'  OR  UPPER(PROGRAM) like '%SQR%'  OR  UPPER(PROGRAM) like '%PSRUN%'  OR  UPPER(PROGRAM) like '%PSPRCSRV%'  OR  UPPER(PROGRAM) like '%PSMSTPRC%'  OR  UPPER(PROGRAM) like '%SQLPLUS%'  THEN 'BATCH'
WHEN  UPPER(PROGRAM) like '%PSAPPSRV%'  THEN 'WEB'
WHEN  UPPER(PROGRAM) like '%PSNVS%'  OR  UPPER(PROGRAM) like '%PSQRYSRV%'  OR  UPPER(PROGRAM) like '%PSAESRV.EXE%'  THEN 'REPORTING'
WHEN  UPPER(PROGRAM) like '%RMAN%'  THEN 'BACKUPS'
ELSE 'OTHER' END,
to_char(sample_time,'YYYY-MM-DD')
)
group by MONDAY_DATE
order by MONDAY_DATE;

This summarizes the CPU usage on the database on Mondays during
working hours grouping by program names. It shows which group of 
database clients are consuming the most database cpu resources.

"""

class cpubyprogram():
    def __init__(self,day,start_hour,stop_hour):
        self.day = day.upper()
        self.start_hour = start_hour
        self.stop_hour = stop_hour
        self.labels = []
        self.programs = []
         
    def add_program(self,program,label):
        """ 
        Record a relationship between a program name and
        a meaningful label of your choice. I.e. program=webhost
        label=WEBFARM. Let's you choose a readable label for a 
        group of programs. There is a many to one relationship 
        between program and label. So you can call this multiple
        times with the same label and all client host programss that 
        match and of the program names will have their cpu consolidated
        under the label.
        """
        # labels has only one entry per label
        if label not in self.labels:
            self.labels.append(label)
        # programs has one entry per program.
        # could have multiple entries for the same label
        self.programs.append([label,program.upper()])
        
    def build_case(self):
        """
        This function builds this part of our example SQL statement:
CASE 
WHEN  UPPER(PROGRAM) like '%webhost%'  THEN 'WEBFARM'
WHEN  UPPER(PROGRAM) like '%mobhost%'  THEN 'MOBILE'
ELSE 'OTHER' END

        Does not show in my example but with multiple programs for a 
        label it builds an OR condition before the THEN keywords.

        """
        case_string = "CASE \n"
        for l in self.labels:
            case_string +=  "WHEN "
            first_program = True
            for m in self.programs:
                if m[0] == l:
                    if not first_program:
                       case_string +=  " OR "
                    else:
                       first_program = False
                    case_string += " UPPER(PROGRAM) like '%"+m[1]+"%' "
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
        
        day_column = self.day+'_DATE'
        
        q_string = """select
"""
        q_string += day_column+","
        
        for l in self.labels:
             q_string += "sum(case when LABELS ='"+l+"' then percent_cpu else 0 end) "+l+',\n'
        q_string += "sum(case when LABELS ='OTHER' then percent_cpu else 0 end) OTHER"
        
        q_string += """
from 
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
group by
"""
        q_string += day_column
        q_string += """
order by
""" 
        q_string += day_column

        return q_string

"""

day_history expects the query to have a column named
MONDAY_DATE, TUESDAY_DATE, etc. See comments before cpubyprogram
for example of query that would be passed to day_history's init function.

day_history uses two tables per week day with this naming standard:
    
MONDAYASHcpubyprogram_PERM
MONDAYASHcpubyprogram_TEMP

In this example day is MONDAY and queryname is ASHcpubyprogram.

The _TEMP table saves the output of the query. The query retrieves
the given day's AWR information.

The _PERM table saves this information long term. So, if your site keeps
the 7 days of AWR history the _TEMP table will have 7 days of information
but _PERM will have history as far back as the first run of the query.

It is intended that the query be run daily to monitor performance and that
_PERM will grow and have entries for every day.

"""

class day_history:
    def __init__(self,db_connection,day,queryname,query):
        self.db_connection = db_connection
        self.day = day.upper()
        self.queryname = queryname.upper()
        self.perm_table_name =  self.day+self.queryname+"_PERM"
        self.temp_table_name =  self.day+self.queryname+"_TEMP"
        self.query = query
    def save_day_results(self):
        
        day_column = self.day+'_DATE'
       
        # check if permanent table exists
        
        check_query = "select count(*) from user_tables where table_name ='"
        check_query += self.perm_table_name+"'"
        results = self.db_connection.run_return_all_results(check_query)
        perm_exists = results[0][0] == 1

        # check if temporary table exists
        
        check_query = "select count(*) from user_tables where table_name ='"
        check_query += self.temp_table_name+"'"
        results = self.db_connection.run_return_all_results(check_query)
        temp_exists = results[0][0] == 1
                                
        # create permanent table for results if not already present
        # create temporary table for this run if needed and add rows
        # to permanent table
               
        if not perm_exists:
            # populate new perm table with results of query
            create_string = 'create table '+self.perm_table_name+' as '+self.query
            self.db_connection.run_return_no_results(create_string)
        else:
            # create empty temp table and load with results of query
            if temp_exists:
                drop_string = 'drop table '+self.temp_table_name
                self.db_connection.run_return_no_results(drop_string)
                
            create_string = 'create table '+self.temp_table_name+' as '+self.query
            self.db_connection.run_return_no_results(create_string)
            
            # delete records in perm that are in temp to avoid 
            # inserting duplicates
            delete_string = 'delete from '+self.perm_table_name
            delete_string += ' where '+day_column+' in (select '
            delete_string += day_column+' from '+self.temp_table_name+')'
            self.db_connection.run_return_no_results(delete_string)
           
            # insert temp rows into perm table
            insert_string = 'insert into '+self.perm_table_name
            insert_string += ' select * from '+self.temp_table_name
            self.db_connection.run_return_no_results(insert_string)
            self.db_connection.commit()
            
        """
        Make final select follow this pattern:
            
        select * from     
            (select * from 
                (select * from MONDAYASHcpubyprogram_PERM order by MONDAY_DATE desc) 
            where rownum < 41)
        order by MONDAY_DATE;
        
        This just shows the last 40 rows.
        
        This final select statement queries the perm table returning
        results in the same format as the query but including the 
        stored older values from earlier runs.
        
        """
        query_string="""select * from     
            (select * from 
                (select * from """    
        query_string +=self.perm_table_name+' order by '
        query_string +=day_column
        query_string +=""" desc) 
            where rownum < 41)
        order by """+day_column
                    
        return self.db_connection.run_return_all_results(query_string)
                        
    def get_column_names(self):
        return self.db_connection.get_column_names()
        
# Main program starts here

database,dbconnection = util.script_startup('Database CPU by Application Area')

day=util.input_no_default('Enter day of week: ')
    
user=util.my_oracle_user
 
c = cpubyprogram(day,8,17)
    
lines = util.read_config_file(util.config_dir,database+util.ashcpuprog_file)

for l in lines:
    args = l.split()
    if len(args) == 2:
        c.add_program(args[0],args[1])
    
querytext = c.build_query()
    
h = day_history(dbconnection,day,'ASHcpubyprogram',querytext)
    
results = h.save_day_results()
    
column_names = h.get_column_names()
    
# Load global variables for graph    

# Build list of labels for the bars
           
myplot.xlabels = []
for r in results:
    myplot.xlabels.append(r[0])
        
# Build a list of lists of y values
# and a list of the labels for each y value

myplot.ylists =  []
myplot.ylistlabels = []
    
for i in range(1,len(column_names)):
    yl=[]
    for r in results:
        val = 100.0 * myplot.nonetozero(r[i])
        yl.append(val)
    myplot.ylists.append(yl)
    myplot.ylistlabels.append(column_names[i])

# Misc labels and names

myplot.title = database.upper()+' CPU Working Hours '+day.capitalize()+'s'
myplot.ylabel1 = 'CPU % Utilization'
myplot.yticksuffix = '%'
myplot.filename = day.lower()+'.png'

# Run stacked bar graph
    
myplot.stacked_bar()
