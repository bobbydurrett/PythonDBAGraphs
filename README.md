# PythonDBAGraphs

This is a Python program that displays graphs that
are helpful for Oracle database performance tuning.

Right now it includes 4 graphs:

ashcpu - Shows cpu usage within an Oracle database
         by various parts of the application.

onewait - Shows the average time for an Oracle wait
          event and the number of events per period.
          
simplesqlstat - Show average elapsed versus executions
                for one SQL statement.

allsql - Show average elapsed versus executions
         for all SQL statements.
          
Command line help:

python dbgraphs.py -h

usage: dbgraphs.py [-h] {ashcpu,onewait,simplesqlstat,allsql} {file,screen}

Create a database performance graph

positional arguments:

  {ashcpu,onewait,simplesqlstat,allsql} Name of report
  
  {file,screen} Where to send the graph

optional arguments:
  -h, --help            show this help message and exit

Example:

python dbgraphs.py onewait screen

This creates the onewait graph and sends the output to the screen.

Requirements:

This has only been tested on Windows 7 using 32-bit
Canopy Express and the cx_Oracle package.

https://www.enthought.com/canopy-express/

https://pypi.python.org/pypi/cx_Oracle/5.2.1

Configuration:

The program uses text files stored in a particular directory
as configuration files. On my laptop they are stored in c:\mypython.
You can change this directory for your installation my modifying 
the value of configuration_file_directory in util.py.

The program also puts generated graph files in c:\temp. This 
target directory can be changed by modifying the value set 
for graph_export_directory in myplot.py.

Related blog posts:

http://www.bobbydurrettdba.com/2016/01/06/trying-python-and-pyplot-for-database-performance-graphs/

http://www.bobbydurrettdba.com/2016/01/14/another-python-graph-one-wait-event/

http://www.bobbydurrettdba.com/2016/03/29/python-dba-graphs-github-repository/

Contact:

bobby@bobbydurrettdba.com

