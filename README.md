# PythonDBAGraphs

This is a python program that will generate graphs of various metrics that
are helpful for Oracle database performance tuning.

Right now it includes 3 graphs:

ashcpu - Shows cpu usage within an Oracle database
         by various parts of the application.

onewait - Shows the average time for an Oracle wait
          event and the number of events per period.
          
simplesqlstat - Show average elapsed versus executions
                for one SQL statement.
          
Command line help:

python dbgraphs.py -h

ashcpu:

python dbgraphs.py ashcpu

onewait:

python dbgraphs.py onewait

simplesqlstat:

python dbgraphs.py simplesqlstat

Requirements:

This has only been tested on Windows 7 using 32-bit
Canopy Express and the cx_Oracle package.

Related blog posts:

http://www.bobbydurrettdba.com/2016/01/06/trying-python-and-pyplot-for-database-performance-graphs/

http://www.bobbydurrettdba.com/2016/01/14/another-python-graph-one-wait-event/

http://www.bobbydurrettdba.com/2016/03/29/python-dba-graphs-github-repository/

Contact:

bobby@bobbydurrettdba.com

