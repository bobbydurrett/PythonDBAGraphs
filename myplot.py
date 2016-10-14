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

"""

Global variables for graph functions

xlabels which is a list of dates in the graphs we have now
This isn't a list of the values on the x axis but the labels 
associated with those values.

ylists is a list of lists of yvalues

ylistlabels is a list of lables, one for each member of ylist

title is the graph title

filename is the graph file name - if None it is calculated

ylabel1-4 is the y axis label for subplots 1-4

yticksuffix - added on to the ytick value (% in ashcpu graph)

numticks - number of ticks across x axis

"""

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
        
import numpy as np
import matplotlib.pyplot as plt
import util
   
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
        print "Graph is "+graphfile
        x = raw_input("Hit enter to continue")
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
        print "Fixed color must be r, g, or b"
        return
    
    if fixed_value < 0.0 or fixed_value > 1.0:
        print "Fixed color value must be between 0.0 and 1.0"
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
    plt.autoscale(tight=True)
    plt.show()
    
def trim_x_ticks():
    """
    Cull x labels down to num_ticks ticks
    so they fit on the screen
    """
    num_x_labels = len(xlabels)
    times_per_tick = num_x_labels/numticks
    if times_per_tick < 1:
        times_per_tick = 1
    trimmed_x_labels=[]
    for i in range(0,num_x_labels):
        if i%times_per_tick == 0:
           trimmed_x_labels.append(xlabels[i])
    xtick_locations=range(0,num_x_labels,times_per_tick)
    return (trimmed_x_labels,xtick_locations)

def stacked_bar():
    """
    Stacked bar graph
    """
       
    if len(xlabels) == 0:
        print "No results to graph"
        return
    
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
        p = plt.bar(xvalues, yvalues, width,color=my_colors(list_num+1),bottom=bottomvals)
        plots.append(p)

    plt.ylabel(ylabel1)
    plt.title(title)

    # xnames is a list of dates based on the first column in the result set
    xnames = xlabels

    # puts the tick marks and dates as labels under the bars
    plt.xticks(xvalues + width/2., xnames,rotation=45)

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
    
    if yticksuffix <> None:
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
        
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)
    
# cull date and time x ticks down to num_ticks ticks
# so they fit on the screen

    trimmed_x_labels,xtick_locations=trim_x_ticks()
           
# do the plot
    plt.title(title)
    plt.ylabel(ylabel1)
    plt.minorticks_on()
    plt.xticks(xtick_locations,trimmed_x_labels,rotation=90)
    plt.grid(which="major")
    
    for plot_num in range(len(ylists)):
         plt.plot(ylists[plot_num],color=my_colors(plot_num))
         
    plt.legend(ylistlabels,loc='upper left')
    plt.autoscale(tight=True)
    
    # subplots_adjust settings - single plot so zero space between plots
    vleft  = 0.05  # the left side of the subplots of the figure
    vright = 0.97    # the right side of the subplots of the figure
    vbottom = 0.12   # the bottom of the subplots of the figure
    vtop = 0.95      # the top of the subplots of the figure
    vwspace = 0.0   # the amount of width reserved for blank space between subplots
    vhspace = 0.0   # the amount of height reserved for white space between subplots

    plt.subplots_adjust(left=vleft,right=vright,bottom=vbottom,top=vtop,wspace=vwspace,hspace=vhspace)

    fileorscreen(title+'.png')
    
    return    
  
def line_2subplots():
    """
    Creates a split plot with one set of x axis labels and
    two subplots.
    
    """
    
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)

# cull date and time x ticks down to num_ticks ticks
# so they fit on the screen

    trimmed_x_labels,xtick_locations=trim_x_ticks()
           
# do the plot
# top half of the graph plot_number 1
    nrows = 2
    ncols = 1
    plot_number = 1   
    plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(ylabel1)
    empty_label_list=[]
    plt.minorticks_on()
    plt.xticks(xtick_locations,empty_label_list)
    plt.grid(which="major")
    red = 'r'
    plt.plot(ylists[0],red)
# bottom half of the graph plot_number 2
    plot_number = 2   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel2)
    plt.minorticks_on()
    plt.xticks(xtick_locations,trimmed_x_labels,rotation=90)
    plt.grid(which="major")
    green='g'
    plt.plot(ylists[1],green)
    
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
    

def line_4subplots():
    """
    Four subplots
        
    """
    
# set the screen title, size, density
    
    plt.figure(title,graph_dimensions,graph_dpi)

# cull date and time x ticks down to num_ticks ticks
# so they fit on the screen

    trimmed_x_labels,xtick_locations=trim_x_ticks()
           
# do the plot
# plot_number 1
    nrows = 2
    ncols = 2
    plot_number = 1   
    plt.subplot(nrows,ncols,plot_number)
    plt.title(title)
    plt.ylabel(ylabel1)
    empty_label_list=[]
    plt.minorticks_on()
    plt.xticks(xtick_locations,empty_label_list)
    plt.grid(which="major")
    red = 'r'
    plt.plot(ylists[0],red)
# plot_number 2
    plot_number = 2   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel2)
    plt.minorticks_on()
    plt.xticks(xtick_locations,empty_label_list)
    plt.grid(which="major")
    green='g'
    plt.plot(ylists[1],green)
# plot_number 3
    plot_number = 3   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel3)
    plt.minorticks_on()
    plt.xticks(xtick_locations,trimmed_x_labels,rotation=90)
    plt.grid(which="major")
    blue = 'b'
    plt.plot(ylists[2],blue)
# plot_number 4
    plot_number = 4   
    plt.subplot(nrows,ncols,plot_number)
    plt.ylabel(ylabel4)
    plt.minorticks_on()
    plt.xticks(xtick_locations,trimmed_x_labels,rotation=90)
    plt.grid(which="major")
    yellow='y'
    plt.plot(ylists[3],yellow)
    
# subplots_adjust settings
    vleft  = 0.07  # the left side of the subplots of the figure
    vright = 0.97    # the right side of the subplots of the figure
    vbottom = 0.15   # the bottom of the subplots of the figure
    vtop = 0.95      # the top of the subplots of the figure
    vwspace = 0.1   # the amount of width reserved for blank space between subplots
    vhspace = 0.08   # the amount of height reserved for white space between subplots

    plt.subplots_adjust(left=vleft,right=vright,bottom=vbottom,top=vtop,wspace=vwspace,hspace=vhspace)
    
    fileorscreen(title+'.png')
    
    return
