# PythonDBAGraphs

This is a Python program that displays graphs that
are helpful for Oracle database performance tuning.

## PythonDBAGraphs includes these graphs:

* `ashcpu.py` - Shows cpu usage within an Oracle database by various parts of the application.

* `onewait.py` - Shows the average time for an Oracle wait event and the number of events per period.
          
* `simplesqlstat.py` - Show average elapsed versus executions for one SQL statement.

* `allsql.py` - Show average elapsed versus executions for all SQL statements.
         
* `groupsigs.py` - Show average elapsed versus executions for SQL statements whose force matching signature is in a specified group of signatures.
          
* `sigscpuio.py` - Show total elapsed, CPU, and IO time for SQL statements whose force matching signature is in a specified group of signatures.

* `sigselapctcpu.py` - Show total elapsed for SQL statements whose force matching signature is in a specified group of signatures. Show percent CPU used on same graph.

* `sigfour.py` - Four metrics for SQL statements whose force matching signature is in a specified group of signatures. These are number of executions, average elapsed time, CPU percent used, and average single block read time.
          
* `ashcount.py` - For a time range show the number of active sessions on CPU and total number active.

* `sqlstatwithplans.py` - Show execution time of a single SQL statement by plan.
                      
* `sessioncounts.py` - Plot the number of connected sessions.

* `segstat.py` - Segment usage statistics for one segment

* `ashonewait.py` - Show the number of sessions active on one particular wait.

* `sqlstatcpuio.py` - Plots total elapsed, cpu, and io seconds for a single sql_id.

* `iosummary.py` - Shows overall I/O information for one database.

* `hostcpu.py` - Shows host level CPU information for one instance

* `onesysstat.py` - Shows a single system statistic for one instance

* `space.py` - Shows overall tablespace usage over time

* `nologging.py` - Write I/O statistics that may relate to nologging write I/O

* `ashcpuprog.py` - Similar to ashcpu.py but using PROGRAM instead of MACHINE. Works with 10.2.

* `activeshared.py` - Average active shared server sessions between AWR snapshots

* `redologs.py` - Number of archived redo logs per hour
          
## Command line help:
```
usage: ashcpu.py [-h] {file,screen} [database] {Y,N} {Y,N}

Database CPU by Application Area

positional arguments:
  {file,screen}  Where to send the graph
  database       Name of the database
  {Y,N}          Show SQL that was executed (Y or N)
  {Y,N}          Show data returned by query (Y or N)

optional arguments:
  -h, --help     show this help message and exit
```
See file `README.md` for more detailed help.

### Example:

`python onewait.py screen ORCL N N`

This creates the onewait.py graph on the ORCL database and sends the output to 
the screen. It does not display the SQL used and it does not output the
data returned by the query.

## Three other included scripts:

* `colorsquares.py` - shows a range of colors. I used this to pick the colors
for the graphs.

### Example:

`python colorsquares.py r .5`

Sets red at 0.5 and shows range of colors varying blue and green between 0.0 and 1.0.

* `show_saved.py` - Displays a graph based on data saved from an earlier run. Prompts for the name of the file that was previously saved.

### Example:

`python show_saved.py`

`Enter name of data file to be restored: D:\temp\All SQL statements on DBATEST2 database.txt`

* `setpassword.py` - Saves an encrypted version of your Oracle password.

### Example:
```
python setpassword.py
Enter password for MYUSER: MYPASSWORD
```

## Requirements:

The author primarily uses this application in the following environment:

* Windows 10

* 32 bit Python 3.7.2

These packages:

* cryptography (2.3.1)
* cx-Oracle (7.0.0)
* cycler (0.10.0)
* matplotlib (3.0.0)
* numpy (1.15.2)
* pip (18.1)
* pyparsing (2.2.2)
* python-dateutil (2.7.3)
* pytz (2018.5)
* setuptools (40.6.2)
* six (1.11.0)
* wxPython (4.0.3)

## Configuration:

The program uses certain directories. The paths to these directories
are stored in the file `directories.txt` which is kept in the same 
location as the `util.py` script. The directories are the configuration, 
password, and output directories.

The configuration directory contains the file `username.txt`
which has the Oracle user name.

It also contains database and graph specific configuration files:

* `DBNAMEashcpufile.txt` - `ashcpu.py` configuration for database DBNAME

* `DBNAMEgroupofsignatures.txt` - SQL signatures for database DBNAME for graphs with "sig" in their name such as `sigscpuio.py`.

The configuration directory also contains a file with the password encryption key.

The password directory contains the password file which stores the
encrypted password.

The output directory is where image files are written if you choose
"file" as the destination for the graph.

You can test these scripts interactively through IDLE by setting the arguments
at the top of the script. So, if you want to test `ashonewait.py` put these lines
at the top of the file:
```
import sys
sys.argv = ['x','screen','YOURDB','N','N']
```
Once you are done testing remove these lines and run the script from the command line.

Related blog posts:

http://www.bobbydurrettdba.com/?s=Python

Contact:

bobby@bobbydurrettdba.com

