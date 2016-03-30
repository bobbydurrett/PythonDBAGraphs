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
        
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

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
    
def plot_cpu_by_day(database,day,results,column_names):
    """
    Plots database cpu history for a day.
    """
        
    number_of_bars = len(results)
    xvalues = np.arange(number_of_bars)    # the x locations for the groups
    width = 0.35       # the width of the bars compared with x index
    
    # get color map so I can use a color for each column's data
    
    number_of_columns = len(column_names)

    cmp = get_cmap(number_of_columns)

    plots = []
    for c in range(1,number_of_columns):
        yvalues=[]
        bottomvals = []
        for r in results:
            yvalues.append(100.0*nonetozero(r[c]))
            btemp=0.0
            for b in range(1,c):
                btemp += 100.0*nonetozero(r[b])
            bottomvals.append(btemp)
        p = plt.bar(xvalues, yvalues, width,color=cmp(c-1),bottom=bottomvals)
        plots.append(p)

    plt.ylabel('CPU % Utilization')
    plt.title(database.upper()+' CPU Working Hours '+day.capitalize()+'s')

    xnames = []
    for row in results:
        xnames.append(row[0])

    plt.xticks(xvalues + width/2., xnames,rotation=45)

    legend_columns = []
    for c in range(1,len(column_names)):
        legend_columns.append(column_names[c].replace("'",""))

    plt.legend(plots, legend_columns,loc='upper left')
    
    plt.grid(axis='y')
    
    locs,labels = plt.yticks()
    new_labels = []
    for l in locs:
        new_labels.append(str(int(l))+'%')
        
    plt.yticks(locs,new_labels)
    
    F = plt.gcf()
    F.set_size_inches((13.,9.))
    graphfile = 'C:\\temp\\'+day.lower()+'.png' 
    plt.savefig(graphfile,dpi = (100))
    print "Graph is "+graphfile
    
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
                   
# cull date and time x ticks down to num_ticks = 30
# so they fit on the screen
    num_ticks=30
    times_per_tick = len(date_time)/num_ticks
    if times_per_tick < 1:
        times_per_tick = 1
    trimmed_date_time=[]
    for i in range(1,len(date_time)):
        if i%times_per_tick == 0:
           trimmed_date_time.append(date_time[i])
    xtick_locations=range(0,len(date_time),times_per_tick)
           
# do the plot
    graph_dimensions=(20,13)
    graph_dpi=75    
    plt.figure(title,graph_dimensions,graph_dpi)
# top half of the graph plot_number 1
    nrows = 2
    ncols = 1
    plot_number = 1   
    plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(top_label)
    empty_label_list=[]
    plt.xticks(xtick_locations,empty_label_list)
    plt.grid()
    red = 'r'
    plt.plot(num_events,red)
# bottom half of the graph plot_number 2
    plot_number = 2   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(bottom_label)
    plt.xticks(xtick_locations,trimmed_date_time,rotation=45)
    plt.grid()
    green='g'
    plt.plot(avg_elapsed,green)
    plt.show()
    
    return