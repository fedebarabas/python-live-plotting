
from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        # load the ui
        self.ui = loadUi('testui.ui', self)
        self.widgetsize = [self.ui.plotwidget.width(), 
                           self.ui.plotwidget.height()]

class DynamicPlotter():

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        # PyQtGraph stuff
        self.plt = window.ui.plotwidget
        
        pg.setConfigOptions(antialias=True)
#        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen='y')
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateplot(self):
        self.databuffer.append( self.getdata() )
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)
#        self.app.processEvents()
        app.processEvents()

    def run(self):
#        self.app.exec_()
        app.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication([])
    
    window = MainWindow()
    window.show()

    m = DynamicPlotter(sampleinterval=0.05, timewindow=10., 
                       size=window.widgetsize)
    m.run()

