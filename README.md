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

This has been primarily tested on Windows 7 using 32-bit
Canopy Express and the cx_Oracle package.

https://www.enthought.com/canopy-express/

https://pypi.python.org/pypi/cx_Oracle/5.2.1

Configuration:

The program uses certain directories. The paths to these directories
is stored in the file directories.txt which is kept in the same 
location as the util.py script. The directories are the configuration, 
password, and output directories.

The configuration directory contains the file userandfilenames.txt
which has the Oracle user name and the file names for the ASH CPU
report configuration and the name of the password file.

The password directory contains the password file. It has lines in this 
format:

Database name:user name:password

The output directory is where image files are written if you choose
"file" as the destination for the graph.

Related blog posts:

http://www.bobbydurrettdba.com/2016/01/06/trying-python-and-pyplot-for-database-performance-graphs/

http://www.bobbydurrettdba.com/2016/01/14/another-python-graph-one-wait-event/

http://www.bobbydurrettdba.com/2016/03/29/python-dba-graphs-github-repository/

Contact:

bobby@bobbydurrettdba.com

Linux configuration:

Recently tested this on Linux virtual machine following this high level outline:

Here are the steps to use PythonDBAGraphs on Linux. Tested on Oracle Enterprise
Linux, a variant of Red Hat.

1 Install Oracle linux 6 as software development workstation.
Run yum update to get current.

2 Install Oracle 11.2.0.4 client using database server yum package. Setup the 
needed Oracle directories. Setup tnsnames.ora entry for test database
and test connection with sqlplus.

3 Use yum to install tcl* and tk*

4 Build python 2.7.11 from source and install.

5 Build matplotlib from source and install.
Set backend to tkagg in matplotlibrc. Use

python s.py --verbose-helpful 

to find the rc file.

s.py:

from pylab import *
plot([1,2,3])
show()

6 Build numpy from source and install.

7 Build cx_Oracle from source and install.

8 Clone PythonDBAGraphs repository using git.

9 Test application. Setup configuration files
to use SYSTEM user and Linux file paths.

