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

saveawr.py

Code relating to saving awr history

"""

import db

"""

day_history expects the query to have a column named
MONDAY_DATE, TUESDAY_DATE, etc. See comments before perfq.cpubymachine
for example of query that would be passed to day_history's init function.

day_history uses two tables per week day with this naming standard:
    
MONDAYASHCPUBYMACHINE_PERM
MONDAYASHCPUBYMACHINE_TEMP

In this example day is MONDAY and queryname is ASHCPUBYMACHINE.

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
                (select * from MONDAYASHCPUBYMACHINE_PERM order by MONDAY_DATE desc) 
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

