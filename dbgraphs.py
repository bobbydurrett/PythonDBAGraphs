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

dbgraphs.py

Top level script to give option to run various graphs.

"""

import argparse
import db
import saveawr
import perfq
import myplot
import util

"""

Load the directory names, file names, and Oracle user name.

"""

util.load_configuration()

# global variable holding database name

database='ORCL'

def ashcpu():

    """
    Generates a graph that shows cpu usage within an Oracle database
    by various parts of the application. The graph is configured by lines in 
    the text file ashcpufile.txt.
    
    Each line is part of a client machine name and a label
    for machines with that pattern.
    
    For example:
    
    abcd WEBFARM
    
    Any client machines with the string abcd in their name 
    will have their database cpu usage grouped into the category WEBFARM.
    
    The graph is hard coded to only look at CPU usage between 8 am and 5 pm
    of the day of the week specified. This is intended to look at CPU usage
    during the work day.
    
    """

    day=raw_input('Enter day of week: ')
    
    user=util.my_oracle_user
     
    c = perfq.cpubymachine(day,8,17)
    
    lines = util.read_config_file(util.config_dir,database+util.ashcpu_file)

    for l in lines:
        args = l.split()
        if len(args) == 2:
            c.add_machine(args[0],args[1])
    
    querytext = c.build_query()
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    d = db.connection(user,password,database)
    h = saveawr.day_history(d,day,'ASHCPUBYMACHINE',querytext)
    
    results = h.save_day_results()
    
    column_names = h.get_column_names()
           
    myplot.plot_cpu_by_day(database,day,results,column_names)
    
def onewait():
    # Get user input
    
    wait_event=util.input_with_default('wait event','db file sequential read')
    min_waits=int(util.input_with_default('minimum number of waits per hour','0'))
    
    # Use my db login credentials
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    
    # Build and run query
    
    q = perfq.onewait(wait_event,min_waits);
    
    c = db.connection(user,password,database)
    
    r = c.run_return_flipped_results(q)
    
    # plot query
        
    title = "'"+wait_event+"' waits on "+database+" database, minimum waits="+str(min_waits)
    top_label = "Number of events"
    bottom_label = "Averaged Elapsed Microseconds"
    
    date_time=r[0]
    num_events=r[1]
    avg_elapsed=r[2]
    
    myplot.frequency_average(title,top_label,bottom_label,
                          date_time,num_events,avg_elapsed)
                          
def simplesqlstat():
    # Get user input
    
    sql_id=util.input_with_default('SQL_ID','acrg0q0qtx3gr')
    
    # Use my db login credentials
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    
    # Build and run query
    
    q = perfq.simplesqlstat(sql_id);
    
    c = db.connection(user,password,database)
    
    r = c.run_return_flipped_results(q)
    
    # plot query
        
    title = "Sql_id "+sql_id+" on "+database+" database"
    top_label = "Number of executions"
    bottom_label = "Averaged Elapsed Milliseconds"
    
    date_time=r[0]
    executions=r[1]
    avg_elapsed=r[2]
    
    myplot.frequency_average(title,top_label,bottom_label,
                          date_time,executions,avg_elapsed)

def allsql():
   
    # Use my db login credentials
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    
    # Build and run query
    
    q = perfq.allsql();
    
    c = db.connection(user,password,database)
    
    r = c.run_return_flipped_results(q)
    
    # plot query
        
    title = "All SQL statements on "+database+" database"
    top_label = "Number of executions"
    bottom_label = "Averaged Elapsed Milliseconds"
    
    date_time=r[0]
    executions=r[1]
    avg_elapsed=r[2]
    
    myplot.frequency_average(title,top_label,bottom_label,
                          date_time,executions,avg_elapsed)

def groupsigs():

    """
    This shows the average elapsed time and total number of executions for 
    a group of SQL statements defined by their force matching signature.
    A signature represents a group of queries that are the same except for their
    constants. The goal of this query is to pick some group of queries 
    that we care about such as the main queries the users use every day and
    show their performance over time. It does hide the details of the individual
    queries but may have value if we choose the best set of signatures.   
    """

    user=util.my_oracle_user
     
    queryobj = perfq.groupofsignatures()
    
    lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

    for line in lines:
        if len(line) > 0:
            queryobj.add_signature(int(line))
    
    querytext = queryobj.build_query()
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    dbconn = db.connection(user,password,database)
    
    results = dbconn.run_return_flipped_results(querytext)
    
    if results == None:
        print "No results returned"
        return
    
    # plot query
        
    title = "SQL matching group of signatures on "+database+" database"
    top_label = "Number of executions"
    bottom_label = "Averaged Elapsed Microseconds"
    
    date_time=results[0]
    executions=results[1]
    avg_elapsed=results[2]
    
    myplot.frequency_average(title,top_label,bottom_label,
                          date_time,executions,avg_elapsed)
def sigscpuio():

    """
    Plots elapsed, cpu, and io for a group of sql statements based
    on their signatures.  
    """

    user=util.my_oracle_user
     
    queryobj = perfq.groupofsignatures()
    
    lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

    for line in lines:
        if len(line) > 0:
            queryobj.add_signature(int(line))
    
    querytext = queryobj.build_query2()
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    dbconn = db.connection(user,password,database)
    
    results = dbconn.run_return_flipped_results(querytext)
    
    if results == None:
        print "No results returned"
        return
    
    # plot query
        
    title = "SQL matching group of signatures on "+database+" database"
    y_label = "Seconds"
        
    number_of_plots=3
    
    plot_names=["Elapsed","CPU","IO"]
    
    myplot.plotmulti(title,y_label,number_of_plots,
                     plot_names,results)

def sigselapctcpu():

    """
    Plots elapsed for a group of sql statements based
    on their signatures against percent CPU of the host. 
    """

    user=util.my_oracle_user
     
    queryobj = perfq.groupofsignatures()
    
    lines = util.read_config_file(util.config_dir,database+util.groupsigs_file)

    for line in lines:
        if len(line) > 0:
            queryobj.add_signature(int(line))
    
    querytext = queryobj.build_query3()
    
    user=util.my_oracle_user
    password=util.get_oracle_password(database)
    dbconn = db.connection(user,password,database)
    
    results = dbconn.run_return_flipped_results(querytext)
    
    if results == None:
        print "No results returned"
        return
    
    # plot query
        
    title = "SQL matching group of signatures on "+database+" database"
    y_label = "Minutes versus Percentage"
        
    number_of_plots=2
    
    plot_names=["CPU % Busy","Elapsed in Minutes"]
    
    myplot.plotmulti(title,y_label,number_of_plots,
                     plot_names,results)

parser = argparse.ArgumentParser(description='Create a database performance graph')
parser.add_argument('reportname', choices=['ashcpu', 'onewait','simplesqlstat','allsql','groupsigs','sigscpuio','sigselapctcpu'], 
                   help='Name of report')
parser.add_argument('destination', choices=['file', 'screen'], 
                   help='Where to send the graph')
parser.add_argument('database',default=None,nargs='?',
                   help='Name of the database')
                   

args = parser.parse_args()

if args.database <> None:
    database = args.database.upper()
else:
    database=util.input_with_default('database','ORCL')

myplot.destination = args.destination
if args.reportname == 'ashcpu':
    ashcpu()
elif args.reportname == 'onewait':
    onewait()
elif args.reportname == 'simplesqlstat':
    simplesqlstat()
elif args.reportname == 'allsql':
    allsql()
elif args.reportname == 'groupsigs':
    groupsigs()
elif args.reportname == 'sigscpuio':
    sigscpuio()
elif args.reportname == 'sigselapctcpu':
    sigselapctcpu()

