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

db.py

Oracle database related code

"""

import cx_Oracle
import sys

# Flag to show SQL statements as they are executed or not.
# Either N or Y.

showsql='N'

# Flag to show data returned from queries or not.
# Either N or Y.

showdata='N'

# connection is single connection to database
# single open cursor

class connection:
    def __init__(self,username,password,database):
        """ Login to database and open cursor """
        connect_string = username+'/'+password+'@'+database
        try:
            self.con = cx_Oracle.connect(connect_string)
        except cx_Oracle.DatabaseError as e:
            print "Error logging in: "+str(e.args[0])
            print "Username: "+username
            print "Password: "+password
            print "Database: "+database
            sys.exit(-1)
        self.cur = self.con.cursor()
        self.column_names=[]
    
    def __del__(self):
        """ Close cursor and connection """
        try:
            self.cur.close()
            self.con.close()
        except:
            return

    def print_data(self,column_names,data_list):
        """ 
        Print a nicely formatted version of
        the data returned by the query.
        """

# Get the maximum length of each column as a string

        num_columns = len(column_names)

# Initialize lengths to column lengths

        max_lengths=[]
        for cn in range(num_columns):
            max_lengths.append(len(column_names[cn]))
            
# Loop through entire list

        for d in data_list:
            for cn in range(num_columns):
                data_length = len(str(d[cn]))
                if data_length > max_lengths[cn]:
                   max_lengths[cn] = data_length
                   
# Print column names padding for max lengths 

        column_name_header=""
        for cn in range(num_columns):
            column_name_header += column_names[cn].rjust(max_lengths[cn]) + " "
        print column_name_header
            
# Print data with same padding
        for d in data_list:
            data_line=""
            for cn in range(num_columns):
                data_line += str(d[cn]).rjust(max_lengths[cn]) + " "
            print data_line
        
    def run_return_all_results(self,query):
        """ 
        Run the SQL Query and return all of the results.
        Returns a list of tuples.
        Each tuple contains one row of query output.
        """
        if showsql == 'Y':
            print query
            
        self.cur.execute(query)
        
        returned_list = []
       
        for result in self.cur:
            returned_list.append(result)
        
        self.column_names=[]
        for d in self.cur.description:
            self.column_names.append(d[0])
            
        if showdata == 'Y':
            self.print_data(self.column_names,returned_list)

        return returned_list
 
    def get_column_names(self):
        """ 
        Return a list of the names of the
        columns returned by the query.
        """
        return self.column_names

    def run_return_no_results(self,non_query):
        """ 
        Execute a SQL statement that does not
        return any results such as DDL, DML.
        In other words run something that is not
        a query.
        """
        if showsql == 'Y':
            print non_query

        self.cur.execute(non_query)
        return

    def commit(self):
        """ Commit all current changes to the database """
        self.con.commit()
        
    def run_return_flipped_results(self,query):
        """
        Method run_return_all_results returns the query results as a 
        list of tuples. For graphing it can help to have each column's 
        values in a list by itself. So this method returns the query 
        results as a list of lists of column values.
        
        r is a list of tuples each tuple is (c1,c2,...)
        want a list of lists of columns
        [[c1 c1 c1 ...][c2 c2 c2 ...]...]
        
        """
        r = self.run_return_all_results(query)
        
        if len(r) == 0:
            return None
        
        number_columns = len(r[0])

        # create a list of empty lists
    
        list_output = []

        for i in range(number_columns):
            list_output.append([])
    
        # append each column to its list

        for curr_row in r:
            for i in range(number_columns):
               list_output[i].append(curr_row[i])

        return list_output

