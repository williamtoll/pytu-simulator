from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        self.graphWidget = pg.PlotWidget()
        #self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)
        #self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

#        self.graphWidget = pg.PlotWidget()
#        self.setCentralWidget(self.graphWidget)

#        self.graphWidget.setTitle("Presion vs Volumen");

#        self.x = list(range(100))  # 100 time points
#        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

#        self.graphWidget.setBackground('w')

#        pen = pg.mkPen(color=(255, 0, 0))
#        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        
#        self.graphWidget.setTitle("Presion vs Volumen");

#        self.x = list(range(100))  # 100 time points
#        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

#        self.graphWidget.setBackground('w')

#        pen = pg.mkPen(color=(255, 0, 0))
#        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        
#        # ... init continued ...
#        self.timer = QtCore.QTimer()
#        self.timer.setInterval(500)
#        self.timer.timeout.connect(self.update_plot_data)
#        self.timer.start()



    def plot(self, presure, time):
        self.graphWidget.plot(presure, time)
    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
