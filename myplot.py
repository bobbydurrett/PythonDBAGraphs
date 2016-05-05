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

myplot.py

My plotting routines

"""

"""

Dimensions for a graph. Corresponds to 1920x1080.
A change here to affect all graphs. 

graph_dimensions is supposed to be in inches and
graph_dpi is dots per inch. Chose these to multiply
to 1920x1080 for HD monitor.

"""

graph_dimensions=(19.2,10.8)
graph_dpi=100

# destination is where the graph will go - screen or file
# set in dbgraphs.py

destination='screen'
        
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import util

# from http://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='prism') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color
    
def nonetozero(value):
    """
    Returns 0.0 if passed None.
    """
    if value == None:
        return 0.0
    else:
        return value

def fileorscreen(filename):
    if destination == 'file':
        graphfile = util.output_dir+filename 
        plt.savefig(graphfile,dpi = (graph_dpi))
        plt.close()
        print "Graph is "+graphfile
        x = raw_input("Hit enter to continue")
    elif destination == 'screen':
        plt.show()
    
def plot_cpu_by_day(database,day,results,column_names):
    """
    Plots database cpu history for a day.
    """
       
    if len(results) == 0:
        print "No results to graph"
        return
    
    title = database.upper()+' CPU Working Hours '+day.capitalize()+'s'
    
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)
 
    number_of_bars = len(results)
    xvalues = np.arange(number_of_bars)    # the x locations for the groups
    width = 0.35       # the width of the bars compared with x index
    
    # get color map so I can use a color for each column's data
    
    number_of_columns = len(column_names)

    cmp = get_cmap(number_of_columns)
    
    # Each level of the bar graph is a plot which is a member of the list
    # plots. Each plot represents a specific class of machines. Each class
    # is a different column in the results returned by the query. So there
    # is one bar plot for each column of the results except the first one 
    # which is just the date.
    plots = []
    for c in range(1,number_of_columns):
        # yvalues is the top of the bar for a given color
        # bottomvals is the bottom of the bar which is stacked
        # on other bars if not the first one.
        yvalues=[]
        bottomvals = []
        # loop through all of the rows in the result set
        for r in results:
            # Use the value for the current column as the top of the bar
            yvalues.append(100.0*nonetozero(r[c]))
            # Calculate the value for the bottom of the bar in btemp
            # Add up previous columns for this row of the result set
            btemp=0.0
            for b in range(1,c):
                btemp += 100.0*nonetozero(r[b])
            bottomvals.append(btemp)
        # draw the next color in the stack of bars and save on the plots list
        p = plt.bar(xvalues, yvalues, width,color=cmp(c-1),bottom=bottomvals)
        plots.append(p)

    plt.ylabel('CPU % Utilization')
    plt.title(title)

    # xnames is a list of dates based on the first column in the result set
    xnames = []
    for row in results:
        xnames.append(row[0])

    # puts the tick marks and dates as labels under the bars
    plt.xticks(xvalues + width/2., xnames,rotation=45)

    # The next section of code builds the legend for each bar of 
    # a given color. The column names are the legend. These represent
    # a meaningful label for a group of machine names of client machines
    # that are accessing the database. For example, one label could be
    # WEBFARM to represent database activity from the web servers.
    legend_columns = []
    for c in range(1,len(column_names)):
        legend_columns.append(column_names[c].replace("'",""))

    plt.legend(plots, legend_columns,loc='upper left')
    
    # put up a grid with a y axis
    
    plt.grid(axis='y')
    
    # this code takes the default labels for the y tick marks
    # and adds a percent sign (%). The values reprecent percent
    # cpu utilization but without this code there would be no
    # % after the number
    
    locs,labels = plt.yticks()
    new_labels = []
    for l in locs:
        new_labels.append(str(int(l))+'%')
        
    plt.yticks(locs,new_labels)
    
    # Produce the image
    
    plt.autoscale(tight=True)
    fileorscreen(day.lower()+'.png')
    
    return
  
def frequency_average(title,top_label,bottom_label,
                      date_time,num_events,avg_elapsed):
    """
    Creates a split plot with date and time as the x axis and
    two subplots.
    
    The top subplot shows how many time or the relative size of the 
    thing being plotted. This could be number of wait events, executions
    seconds of cpu, etc.
    
    The bottom subplot is the average per execution. Could be execution time,
    wait time, cpu time, etc.
    
    Inputs:
        title - title across the top of the plot
        top_label - y label on top subplot
        bottom_label - y label on bottom subplot
        date_time - date and time of sample - list
        num_events - number of events (waits, etc.) - list
        avg_elapsed - average elapsed time - list
    
    """
    
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)

# cull date and time x ticks down to num_ticks ticks
# so they fit on the screen
    num_ticks=25
    times_per_tick = len(date_time)/num_ticks
    if times_per_tick < 1:
        times_per_tick = 1
    trimmed_date_time=[]
    for i in range(0,len(date_time)):
        if i%times_per_tick == 0:
           trimmed_date_time.append(date_time[i])
    xtick_locations=range(0,len(date_time),times_per_tick)
           
# do the plot
# top half of the graph plot_number 1
    nrows = 2
    ncols = 1
    plot_number = 1   
    plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(top_label)
    empty_label_list=[]
    plt.minorticks_on()
    plt.xticks(xtick_locations,empty_label_list)
    plt.grid(which="major")
    red = 'r'
    plt.plot(num_events,red)
# bottom half of the graph plot_number 2
    plot_number = 2   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(bottom_label)
    plt.minorticks_on()
    plt.xticks(xtick_locations,trimmed_date_time,rotation=90)
    plt.grid(which="major")
    green='g'
    plt.plot(avg_elapsed,green)
    
# subplots_adjust settings
    vleft  = 0.07  # the left side of the subplots of the figure
    vright = 0.97    # the right side of the subplots of the figure
    vbottom = 0.15   # the bottom of the subplots of the figure
    vtop = 0.95      # the top of the subplots of the figure
    vwspace = 0.0   # the amount of width reserved for blank space between subplots
    vhspace = 0.08   # the amount of height reserved for white space between subplots

    plt.subplots_adjust(left=vleft,right=vright,bottom=vbottom,top=vtop,wspace=vwspace,hspace=vhspace)
    
    fileorscreen(title+'.png')
    
    return
