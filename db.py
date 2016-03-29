# Oracle database related code

import cx_Oracle

# connection is single connection to database
# single open cursor

class connection:
    def __init__(self,username,password,database):
        """ Login to database and open cursor """
        connect_string = username+'/'+password+'@'+database
        self.con = cx_Oracle.connect(connect_string)
        self.cur = self.con.cursor()
        self.column_names=[]
    
    def __del__(self):
        """ Close cursor and connection """
        self.cur.close()
        self.con.close()

    def run_return_all_results(self,query):
        """ 
        Run the SQL Query and return all of the results.
        Returns a list of tuples.
        Each tuple contains one row of query output.
        """
        self.cur.execute(query)
        
        returned_list = []
       
        for result in self.cur:
            returned_list.append(result)
        
        self.column_names=[]
        for d in self.cur.description:
            self.column_names.append(d[0])

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

