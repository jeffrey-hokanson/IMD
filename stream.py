#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# (c) Jeffrey M. Hokanson 
# Started 4 June 2014

"""
Shows a view of each channel in an IMD file, displayed as a row in a multiline plot.
To move the plot left and right, use the left and right arrow keys.

Usage:
./stream.py <IMD file>

Requirements:
imd.py
matplotlib, numpy

"""




import imd
import matplotlib
matplotlib.use("QT4agg")
#matplotlib.use("wxagg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sys



if __name__ == "__main__":
    # Open file
    filename = sys.argv[1]
    data = imd.read(filename)

    # Location to start reading and how much data to show on each step
    start = 0
    step = 1000

    # Prepare plot window with a row for each tag
    fig = plt.figure()#tight_layout = True)
    gs = gridspec.GridSpec(data.ncol,1, wspace = 5.0, hspace = 0.0)
    ax = []
    for j in range(data.ncol):
        ax.append(plt.subplot(gs[j,0]))

    fig.subplots_adjust(left = 0.02, right = 0.98, top = 1, bottom = 0.02)
   

    def plot():
        """ Draw the plot 
        """
        global start, step, ax, fig, data
        
        x = data[start:start+step]
        tot = x.sum(axis = 1)
        time = np.arange(start, start+step)
        for j in range(data.ncol):
            ax[j].cla()
            ax[j].plot(time, x[:,j],'k')
            #ax[j].set_ylim(bottom=0, top=50)
            ax[j].spines['bottom'].set_color('white')
            ax[j].spines['top'].set_color('white')
            ax[j].set_yticklabels([], visible = False)
            ax[j].set_ylabel(data.tags[j])
            if j != data.ncol - 1:
                ax[j].set_xticklabels([], visible = False)
        ax[0].figure.canvas.draw()
 

    def move(event):
        """
        Function called by matplotlib callback that moves the displayed data left and right
        """
        global start, step, ax, fig, data
        print 'key = {}'.format(event.key)
        if event.key in ['ctrl+c', 'ctrl+C']:
             sys.exit(0)
        
        if event.key == 'right':
            start += step
        if event.key == 'left':
            start -= step
            start = max(0, start)
        
        if event.key in ['left', 'right']:
            plot()
        

    cid = fig.canvas.mpl_connect('key_press_event', move)
    # Draw first frame
    plot()
    
    # Maximize window
    mgr = plt.get_current_fig_manager()
    print matplotlib.get_backend()
    if matplotlib.get_backend() == 'wxagg':
        mgr.frame.Maximize(True)
    if matplotlib.get_backend() =='Qt4Agg':
        mgr.window.showMaximized()
    
    plt.show()



