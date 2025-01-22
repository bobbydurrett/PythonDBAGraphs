import cx_Oracle
import numpy as np
import matplotlib.pyplot as plt
import sys

# get database login information from command line
# username password database
# database has to be a tnsnames.ora file entry

if len(sys.argv) != 4:
    print("Arguments: username password database")
    sys.exit()

username=sys.argv[1]
password=sys.argv[2]
database=sys.argv[3]

# get day of week, hour of day, and cpu percent used
# from DBA_HIST_OSSTAT

query= """
with
myoscpu as
(select
busy_v.SNAP_ID,
busy_v.VALUE BUSY_TIME,
idle_v.VALUE IDLE_TIME
from 
DBA_HIST_OSSTAT busy_v,
DBA_HIST_OSSTAT idle_v
where
busy_v.SNAP_ID = idle_v.SNAP_ID AND
busy_v.DBID = idle_v.DBID AND
busy_v.INSTANCE_NUMBER = idle_v.INSTANCE_NUMBER AND
busy_v.STAT_NAME = 'BUSY_TIME' AND
idle_v.STAT_NAME = 'IDLE_TIME'),
myoscpudiff as
(select
after.SNAP_ID,
(after.BUSY_TIME - before.BUSY_TIME) BUSY_TIME,
(after.IDLE_TIME - before.IDLE_TIME) IDLE_TIME 
from 
myoscpu before,
myoscpu after
where before.SNAP_ID + 1 = after.SNAP_ID
order by before.SNAP_ID)
select 
to_number(to_char(sn.END_INTERVAL_TIME,'D')) day_of_week,
to_number(to_char(sn.END_INTERVAL_TIME,'HH24')) hour_of_day,
100*BUSY_TIME/(BUSY_TIME+IDLE_TIME) pct_busy
from 
myoscpudiff my,
DBA_HIST_SNAPSHOT sn
where 
my.SNAP_ID = sn.SNAP_ID
order by my.SNAP_ID
"""

# run query retrieve all rows

connect_string = username+'/'+password+'@'+database
con = cx_Oracle.connect(connect_string)
cur = con.cursor()

cur.execute(query)

# returned is a list of tuples
# with int and float columns
# day of week,hour of day, and cpu percent

returned = cur.fetchall()

print("Data type of returned rows and one row")
print(type(returned))
print(type(returned[0]))

print("Length of list and tuple")
print(len(returned))
print(len(returned[0]))

print("Data types of day of week, hour of day, and cpu percent")
print(type(returned[0][0]))
print(type(returned[0][1]))
print(type(returned[0][2]))
       
cur.close()
con.close()

# change into numpy array and switch columns
# and rows so there are three rows and many columns
# instead of many rows and three columns

dataarray = np.array(returned).transpose()

# dataarray[0] is day of week
# dataarray[1] is hour of day
# dataarray[2] is cpu percent

print("Shape of numpy array after converting returned data and transposing rows and columns")
print(dataarray.shape)

print("Data type of transposed and converted database data and of the first row of that data")
print(type(dataarray))
print(type(dataarray[0]))

print("Data type of the first element of each of the three transposed rows.")
print(type(dataarray[0][0]))
print(type(dataarray[1][0]))
print(type(dataarray[2][0]))

# do 24 * day of week + hour of day as x axis

xarray = (dataarray[0] * 24) + dataarray[1]

# pull cpu percentage into its own array

yarray = dataarray[2]

print("Shape of numpy x and y arrays")
print(xarray.shape)
print(yarray.shape)

# point_size is size of points on the graph

point_size = 5.0

# get figure and axes

fig, ax = plt.subplots()

# graph the points setting them all to one size

ax.scatter(xarray, yarray, s=point_size)

# add title

ax.set_title(database+" database CPU by day of week and hour of day")

# label the x and y axes

ax.set_xlabel("24 * Day of week (1-7) + Hour of day (0-23)")
ax.set_ylabel("CPU percent used")

# add vertical red lines for days

for day_of_week in range(8):
    ax.axvline(x=(day_of_week+1)*24, color='red', linestyle='--',linewidth=1.0)
    
# add day names

# Calculate the y-coordinate for day names
# It should be a fraction of the range between the minimum and maximum Y values
# positioned below the lower bound of the graph.
# The minimum and maximum CPU varies depending on the load on the queried database.

lower_bound = ax.get_ylim()[0]
upper_bound = ax.get_ylim()[1]
yrange = upper_bound - lower_bound
fraction = .025
y_coord = lower_bound - (fraction * yrange)

xloc = 36

for day in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']:
    ax.text(xloc, y_coord, day, fontsize=8, color='red', ha='center',fontweight='ultralight')
    xloc += 24

# show graph

plt.show()

"""

Helpful Matplotlib documentation that
covers these routines:

Quick Start:

https://matplotlib.org/stable/users/explain/quick_start.html

Axes URL

https://matplotlib.org/stable/api/axes_api.html

"""


