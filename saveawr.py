"""
code relating to saving awr history
"""

import db

# day_history expects the query to have a column named
# MONDAY_DATE, TUESDAY_DATE, etc.

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
            create_string = 'create table '+self.perm_table_name+' as '+self.query
            self.db_connection.run_return_no_results(create_string)
        else:
            if temp_exists:
                drop_string = 'drop table '+self.temp_table_name
                self.db_connection.run_return_no_results(drop_string)
                
            create_string = 'create table '+self.temp_table_name+' as '+self.query
            self.db_connection.run_return_no_results(create_string)
            
            delete_string = 'delete from '+self.perm_table_name
            delete_string += ' where '+day_column+' in (select '
            delete_string += day_column+' from '+self.temp_table_name+')'
            self.db_connection.run_return_no_results(delete_string)
           
            insert_string = 'insert into '+self.perm_table_name
            insert_string += ' select * from '+self.temp_table_name
            self.db_connection.run_return_no_results(insert_string)
            self.db_connection.commit()
            
        query_string ='select * from '+self.perm_table_name+' order by '
        query_string +=day_column
                    
        return self.db_connection.run_return_all_results(query_string)
                        
    def get_column_names(self):
        return self.db_connection.get_column_names()

