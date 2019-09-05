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

nologging.py

Shows possible nologging write I/O in time period. 

"""

import myplot
import util

def nologging(start_time,end_time,instance_number):
    """
    NOLOGGING activity by snapshot
    """
    q_string = """
    
select 
sn.END_INTERVAL_TIME,
(adirect.SMALL_WRITE_MEGABYTES+adirect.LARGE_WRITE_MEGABYTES-bdirect.SMALL_WRITE_MEGABYTES-bdirect.LARGE_WRITE_MEGABYTES)+
(adbwr.SMALL_WRITE_MEGABYTES+adbwr.LARGE_WRITE_MEGABYTES-bdbwr.SMALL_WRITE_MEGABYTES-bdbwr.LARGE_WRITE_MEGABYTES)-
(algwr.SMALL_WRITE_MEGABYTES+algwr.LARGE_WRITE_MEGABYTES-blgwr.SMALL_WRITE_MEGABYTES-blgwr.LARGE_WRITE_MEGABYTES)
from 
DBA_HIST_IOSTAT_FUNCTION bdirect, 
DBA_HIST_IOSTAT_FUNCTION adirect,
DBA_HIST_IOSTAT_FUNCTION bdbwr, 
DBA_HIST_IOSTAT_FUNCTION adbwr,
DBA_HIST_IOSTAT_FUNCTION blgwr, 
DBA_HIST_IOSTAT_FUNCTION algwr,
DBA_HIST_SNAPSHOT sn
where 
adirect.snap_id=bdirect.snap_id+1 and
adirect.snap_id=adbwr.snap_id and
adirect.snap_id=algwr.snap_id and
bdirect.snap_id=bdbwr.snap_id and
bdirect.snap_id=blgwr.snap_id and
bdirect.instance_number=adirect.instance_number and
bdbwr.instance_number=adbwr.instance_number and
blgwr.instance_number=algwr.instance_number and
adirect.snap_id=sn.snap_id and
adirect.instance_number=sn.instance_number and
adirect.FUNCTION_NAME = 'Direct Writes' and
bdirect.FUNCTION_NAME = adirect.FUNCTION_NAME and
adbwr.FUNCTION_NAME = 'DBWR' and
bdbwr.FUNCTION_NAME = adbwr.FUNCTION_NAME and
algwr.FUNCTION_NAME = 'LGWR' and
blgwr.FUNCTION_NAME = algwr.FUNCTION_NAME and
(adirect.SMALL_WRITE_MEGABYTES+adirect.LARGE_WRITE_MEGABYTES-bdirect.SMALL_WRITE_MEGABYTES-bdirect.LARGE_WRITE_MEGABYTES)+
(adbwr.SMALL_WRITE_MEGABYTES+adbwr.LARGE_WRITE_MEGABYTES-bdbwr.SMALL_WRITE_MEGABYTES-bdbwr.LARGE_WRITE_MEGABYTES)-
(algwr.SMALL_WRITE_MEGABYTES+algwr.LARGE_WRITE_MEGABYTES-blgwr.SMALL_WRITE_MEGABYTES-blgwr.LARGE_WRITE_MEGABYTES) >= 0 and
sn.END_INTERVAL_TIME 
between 
to_date('""" 
    q_string += start_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and 
to_date('"""
    q_string += end_time
    q_string += """','DD-MON-YYYY HH24:MI:SS')
and adirect.INSTANCE_NUMBER = """
    q_string += instance_number
    q_string += """
order by sn.END_INTERVAL_TIME
"""
    return q_string

database,dbconnection = util.script_startup('NOLOGGING Write IO')

start_time=util.input_with_default('Start date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-1900 12:00:00')

end_time=util.input_with_default('End date and time (DD-MON-YYYY HH24:MI:SS)','01-JAN-2200 12:00:00')

instance_number=util.input_with_default('Database Instance (1 if not RAC)','1')
 
querytext = nologging(start_time,end_time,instance_number)
    
results = dbconnection.run_return_flipped_results(querytext)

util.exit_no_results(results)

# plot query

myplot.xdatetimes = results[0]
myplot.ylists = results[1:]
    
myplot.title = "NOLOGGING Write IO for "+database+" database, instance "+instance_number
myplot.ylabel1 = "Megabytes"
    
myplot.ylistlabels=["NOLOGGING Writes"]

myplot.line()
