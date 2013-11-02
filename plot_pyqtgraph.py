
from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np

from pint import UnitRegistry
ureg = UnitRegistry()

def amplitude():
    frequency = 0.5
    noise = random.normalvariate(0., 1.)
    new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
    return new * ureg.volt


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        # load the ui
        self.ui = loadUi('testui.ui', self)


class DynamicPlotter():

    def __init__(self, widget, func, sampleinterval=0.1, timewindow=10.):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        
        self.func = func        
      
        self.plt = widget
        
        pg.setConfigOptions(antialias=True)
#        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
        size = [widget.width(), widget.height()]
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', self.func.__name__, self.func().units)
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen='y')
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)
        
    def updateplot(self):
        self.databuffer.append( self.func().magnitude )
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)
        

if __name__ == '__main__':

    
    app = QtGui.QApplication([])
    
    window = MainWindow()
    window.show()

    m = DynamicPlotter(window.ui.plotwidget, amplitude, sampleinterval=0.05, 
                       timewindow=10.)
                       
    app.exec_()

