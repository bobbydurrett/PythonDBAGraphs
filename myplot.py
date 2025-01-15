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

Dimensions for a graph. Corresponds to 1600x900.
A change here to affect all graphs. 

graph_dimensions is supposed to be in inches and
graph_dpi is dots per inch. 

"""

graph_dimensions=(16,9)
graph_dpi=100

# destination is where the graph will go - screen or file
# set in dbgraphs.py

destination='screen'

"""

Global variables for graph functions

xlabels is a list of dates in the graphs.
This isn't a list of the values on the x axis but the labels 
associated with those values.

xdatetimes is a list of dates and times
which form the x axis values for the graphs.

ylists is a list of lists of yvalues

ylistlabels is a list of lables, one for each member of ylist

title is the graph title

filename is the graph file name - if None it is calculated

ylabel1-4 is the y axis label for subplots 1-4

yticksuffix - added on to the ytick value (% in ashcpu graph)

numticks - number of ticks across x axis

"""

xdatetimes = []
xlabels = []
ylists = []
ylistlabels = []
title = "NOT DEFINED"
filename = None
ylabel1 = "NOT DEFINED"
ylabel2 = "NOT DEFINED"
ylabel3 = "NOT DEFINED"
ylabel4 = "NOT DEFINED"
yticksuffix = None
numticks = 25

# flag set to true when doing graph from saved data

restoring_data = False
        
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import util
import myplot

def save_data(plot_name):
    """
    Saves the data for a graph so that it can be redrawn later.
    
    """
    
# Exit if you are displaying an image from saved data
# No need to save the saved data again.
    
    if restoring_data:
        return
    
    save_file=util.open_save_file()
    
# These are the global variables in myplot that are used
# to draw a graph. Saving all of the information that the
# graph functions would use.
    
    util.save_string(save_file,plot_name)
    
    util.save_date_times(save_file,xdatetimes)
    
    util.save_string_list(save_file,xlabels)
    
    util.save_list_list_nums(save_file,ylists)
    
    util.save_string_list(save_file,ylistlabels)
    
    util.save_string(save_file,title)
    util.save_string(save_file,filename)
    util.save_string(save_file,ylabel1)
    util.save_string(save_file,ylabel2)
    util.save_string(save_file,ylabel3)
    util.save_string(save_file,ylabel4)
    util.save_string(save_file,yticksuffix)
    
    util.close_file(save_file)

def restore_data(file_name):
    """
    Restores the data for a graph so that it can be redrawn.
    
    Returns name of plot like line.
    
    """
    
# Set flag so that graph routines know that they are graphing restored data    
    
    myplot.restoring_data = True
    
    restore_file=util.open_restore_file(file_name)
    
# Restores the values of the myplot global variables just as they would be
# if pulled from the database for a graph.
    
    plot_name = util.restore_string(restore_file)
    
    myplot.xdatetimes = util.restore_date_times(restore_file)
        
    myplot.xlabels = util.restore_string_list(restore_file)
    
    myplot.ylists = util.restore_list_list_nums(restore_file)
    
    myplot.ylistlabels = util.restore_string_list(restore_file)
    
    myplot.title = util.restore_string(restore_file)
    myplot.filename = util.restore_string(restore_file)
    myplot.ylabel1 = util.restore_string(restore_file)
    myplot.ylabel2 = util.restore_string(restore_file)
    myplot.ylabel3 = util.restore_string(restore_file)
    myplot.ylabel4 = util.restore_string(restore_file)
    myplot.yticksuffix = util.restore_string(restore_file)
    
    util.close_file(restore_file)
    
    return plot_name
   
def my_colors(colornum):
    """
    Returns a color that can be used in a plot.
    Define a number of colors that I would like to see
    in stacked bar graphs, lines, etc.
    """
    
    mycolorlist=[
    (1.0,0.4,0.4), 
    (0.3,1.0,0.3), 
    (0.3,0.3,1.0),
    (1.0,1.0,0.3), 
    (0.4,0.9,1.0), 
    (1.0,0.4,1.0), 
    (0.5,0.8,0.5),
    (0.6,0.6,0.8)]
      
    num_colors=len(mycolorlist)
    
    return mycolorlist[(colornum%num_colors) - 1]
   
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
        plt.close('all')
        print("Graph is "+graphfile)
        x = util.input_no_default("Hit enter to continue")
    elif destination == 'screen':
        plt.show()

def colorsquares(fixed_color,fixed_value):       
    """
    Shows a range of colors. Used to help choose
    which color (r,g,b) to use in a graph.
    
    Increments of 0.1
    
    Choose one color to be fixed.
    'r','g','b'

    Set that color's value,0.0-1.0.

    """

    if fixed_color not in ['r','g','b']:
        print("Fixed color must be r, g, or b")
        return
    
    if fixed_value < 0.0 or fixed_value > 1.0:
        print("Fixed color value must be between 0.0 and 1.0")
        return
    
    inc = 0.1
    
    if fixed_color == 'r':
        title = "Red fixed "
    elif fixed_color == 'g':
        title = "Green fixed "
    elif fixed_color == 'b':
        title = "Blue fixed "

    title = title + "value = "+str(fixed_value)
    
    # set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)
    
    if fixed_color == 'r':
        plt.ylabel('Green')
        plt.xlabel('Blue')
    elif fixed_color == 'g':
        plt.ylabel('Red')
        plt.xlabel('Blue')
    elif fixed_color == 'b':
        plt.ylabel('Red')
        plt.xlabel('Green')
    
    plt.title(title)

    for yidx in range(11):
        x=[]
        y=[]
        c=[]
        bt=[]
        for xidx in range(11):
            x.append(xidx*inc)
            y.append(inc)
            bt.append(yidx*inc)
            if fixed_color == 'r':
                c.append((fixed_value,yidx*inc,xidx*inc))
            elif fixed_color == 'g':
                c.append((yidx*inc,fixed_value,xidx*inc))
            elif fixed_color == 'b':
                c.append((yidx*inc,xidx*inc,fixed_value))
        plt.bar(x,y,inc,color=c,bottom=bt)
    
    plt.yticks(np.arange(inc/2.0, 1.0+(1.5*inc), 2.0*inc),
               np.arange(0.0, 1.0+inc, 2.0*inc))    
    plt.autoscale(tight=True)
    plt.show()
    
def stacked_bar():
    """
    Stacked bar graph
    """
       
    if len(xlabels) == 0:
        print("No results to graph")
        return

# Save data to redraw plot later
        
    save_data('stacked_bar')
    
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)
 
    number_of_bars = len(xlabels)
    xvalues = np.arange(number_of_bars)    # the x locations for the groups
    width = 0.35       # the width of the bars compared with x index
    
    number_of_ylists = len(ylists)
    plots = []
    for list_num in range(number_of_ylists):
        # yvalues is the top of the bar for a given color
        # bottomvals is the bottom of the bar which is stacked
        # on other bars if not the first one.
        yvalues=ylists[list_num]
        bottomvals = []
        # loop through all of the rows in the result set
        for bar_num in range(number_of_bars):
            # Calculate the value for the bottom of the bar in btemp
            # Add up previous columns for this row of the result set
            btemp=0.0
            for list_num_2 in range(list_num):
                btemp += nonetozero(ylists[list_num_2][bar_num])
            bottomvals.append(btemp)
        # draw the next color in the stack of bars and save on the plots list
        p = plt.bar(xvalues, yvalues, width,color=my_colors(list_num+1),bottom=bottomvals,edgecolor='k',linewidth=0.5,linestyle='solid')
        plots.append(p)

    plt.ylabel(ylabel1)
    plt.title(title)

    # xnames is a list of dates based on the first column in the result set
    xnames = xlabels

    # puts the tick marks and dates as labels under the bars
    plt.xticks(xvalues,xnames,rotation=45)

    # The next section of code builds the legend for each bar of 
    # a given color.
    
    legend_labels = []
    for list_num in range(number_of_ylists):
        legend_labels.append(ylistlabels[list_num].replace("'",""))

    plt.legend(plots,legend_labels,loc='upper left')
    
    # put up a grid with a y axis
    
    plt.grid(axis='y')
    
    # this code takes the default labels for the y tick marks
    # and adds yticksuffix.
    
    if yticksuffix != None:
        locs,labels = plt.yticks()
        new_labels = []
        for l in locs:
            new_labels.append(str(int(l))+yticksuffix)
        
        plt.yticks(locs,new_labels)
    
    # Produce the image
    
    plt.autoscale(tight=True)
    
    if filename == None:
        fileorscreen(title+'.png')
    else:
        fileorscreen(filename)

    return

def line():
    """
    Creates a single graph with date and time as the x axis and
    a variable number of plots.
        
    """
    
# Save data to redraw plot later
        
    save_data('line')
        
# set the screen title, size, density
    
    fig = plt.figure(title,graph_dimensions,graph_dpi)
               
# do the plot

    plt.title(title)
    plt.ylabel(ylabel1)
    plt.grid(which="major")
    
    for plot_num in range(len(ylists)):
         plt.plot(xdatetimes,ylists[plot_num],color=my_colors(plot_num))

# date time formatting

    ax = fig.axes[0]
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    loc=mdates.AutoDateLocator()
    datetimefmt = mdates.AutoDateFormatter(loc)
    ax.xaxis.set_major_formatter(datetimefmt)
    ax.xaxis.set_major_locator(loc)

# other formatting
         
    plt.legend(ylistlabels,loc='upper left')
    plt.autoscale(tight=True)
    
    fileorscreen(title+'.png')
    
    return    
  
def line_2subplots():
    """
    Creates a split plot with one set of x axis labels and
    two subplots.
    
    """

# Save data to redraw plot later
        
    save_data('line_2subplots')
        
# set the screen title, size, density
    
    fig = plt.figure(title,graph_dimensions,graph_dpi)

# do the plot
# top half of the graph plot_number 1
    nrows = 2
    ncols = 1
    plot_number = 1   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(ylabel1)
    plt.grid(which="major")
    red = 'r'
    plt.plot(xdatetimes,ylists[0],red)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    datetimefmt = mdates.DateFormatter('')
    ax.xaxis.set_major_formatter(datetimefmt)
# bottom half of the graph plot_number 2
    plot_number = 2   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel2)
    plt.grid(which="major")
    green='g'
    plt.plot(xdatetimes,ylists[1],green)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    loc=mdates.AutoDateLocator()
    datetimefmt = mdates.AutoDateFormatter(loc)
    ax.xaxis.set_major_formatter(datetimefmt)
    ax.xaxis.set_major_locator(loc)    

    fileorscreen(title+'.png')
       
    return
    
def line_4subplots():
    """
    Four subplots
        
    """

# Save data to redraw plot later
        
    save_data('line_4subplots')
    
# set the screen title, size, density
    
    fig = plt.figure(title,graph_dimensions,graph_dpi)

# do the plot
# plot_number 1
    nrows = 2
    ncols = 2
    plot_number = 1   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(ylabel1)
    plt.grid(which="major")
    red = 'r'
    plt.plot(xdatetimes,ylists[0],red)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    datetimefmt = mdates.DateFormatter('')
    ax.xaxis.set_major_formatter(datetimefmt)
# plot_number 2
    plot_number = 2   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel2)
    plt.grid(which="major")
    green='g'
    plt.plot(xdatetimes,ylists[1],green)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    datetimefmt = mdates.DateFormatter('')
    ax.xaxis.set_major_formatter(datetimefmt)
# plot_number 3
    plot_number = 3   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel3)
    plt.grid(which="major")
    blue = 'b'
    plt.plot(xdatetimes,ylists[2],blue)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    loc=mdates.AutoDateLocator()
    datetimefmt = mdates.AutoDateFormatter(loc)
    ax.xaxis.set_major_formatter(datetimefmt)
    ax.xaxis.set_major_locator(loc)
# plot_number 4
    plot_number = 4   
    ax = plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel4)
    plt.grid(which="major")
    yellow='y'
    plt.plot(xdatetimes,ylists[3],yellow)
    plt.autoscale(tight=True)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%m/%d/%Y %H:%M')
    loc=mdates.AutoDateLocator()
    datetimefmt = mdates.AutoDateFormatter(loc)
    ax.xaxis.set_major_formatter(datetimefmt)
    ax.xaxis.set_major_locator(loc)
        
    fileorscreen(title+'.png')
    
    return
