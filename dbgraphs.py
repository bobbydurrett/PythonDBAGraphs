import argparse
import db
import saveawr
import perfq
import myplot
import util

def ashcpu():

    """
    Generates a graph that shows cpu usage within an Oracle database
    by various parts of the application. The graph is configured by lines in 
    the text file C:\mypython\ashcpufile.txt
    
    The first line of the file is the Oracle database name.
    
    Each additional line is part of a client machine name and a label
    for machines with that pattern.
    
    For example:
    
    MYDB
    abcd WEBFARM
    
    Any client machines of the database MYDB with the string abcd in their name 
    will have their database cpu usage grouped into the category WEBFARM.
    
    The graph is hard coded to only look at CPU usage between 8 am and 5 pm
    of the day of the week specified. This is intended to look at CPU usage
    during the work day.
    
    """

    day=raw_input('Enter day of week: ')
    
    
    m = util.me()
    user=m.my_oracle_username()
    password=m.my_oracle_password()
    
    c = perfq.cpubymachine(day,8,17)
    
    MACHINE_FILE = "C:\\mypython\\ashcpufile.txt"
    inFile = open(MACHINE_FILE, 'r', 0)
    lines = inFile.read().splitlines()
    database=lines.pop(0)
    for l in lines:
        args = l.split()
        c.add_machine(args[0],args[1])
    
    querytext = c.build_query()
    
    d = db.connection(user,password,database)
    h = saveawr.day_history(d,day,'ASHCPUBYMACHINE',querytext)
    
    results = h.save_day_results()
    
    column_names = h.get_column_names()
           
    myplot.plot_cpu_by_day(database,day,results,column_names)
    
    x = raw_input("Hit enter to continue")
    
def onewait():
    # Get user input
    
    database=util.input_with_default('database','ORCL')
    wait_event=util.input_with_default('wait event','db file sequential read')
    min_waits=int(util.input_with_default('minimum number of waits per hour','0'))
    
    # Use my db login credentials
    
    m = util.me()
    user=m.my_oracle_username()
    password=m.my_oracle_password()
    
    # Build and run query
    
    o = perfq.onewait(wait_event,min_waits);
    q = o.build_query()
    
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
    
parser = argparse.ArgumentParser(description='Create a database performance graph')
parser.add_argument('reportname', choices=['ashcpu', 'onewait'], 
                   help='Name of report')

args = parser.parse_args()
if args.reportname == 'ashcpu':
    ashcpu()
elif args.reportname == 'onewait':
    onewait()

