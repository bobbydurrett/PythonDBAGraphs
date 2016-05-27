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

colorsquares.py

Top level script to show variety of colors to choose from.

First argument is one of the primary colors r,g,b to leave fixed
while the other two are varied.

The second argument is a value for the fixed color between
0.0 and 1.0 inclusive.

Draws a square showing the colors in .1 increments.

"""

import argparse
import myplot
import util
    
parser = argparse.ArgumentParser(description='Display colors to choose from')
parser.add_argument('fixed_color', choices=['r', 'g','b'], 
                   help='Primary color to leave fixed')
parser.add_argument('fixed_value',type=float,default=0.0,nargs='?',
                   help='Value of fixed color between 0.0 and 1.0')
                   

args = parser.parse_args()

myplot.colorsquares(args.fixed_color,args.fixed_value)
