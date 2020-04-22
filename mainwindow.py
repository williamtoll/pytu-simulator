from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import serial
import time
from random import randint
from utils import TimeAxisItem, timestamp
import parameters
import snap7
from snap7 import util


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.pmax=60.0
        self.pmin=10.0

        self.pmaxRead=0.0


        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        #load default data
        self.setInitialData()

        self.pushButtonParameter.pressed.connect(self.openParameterWindow)

        ustring=' simple string'
        new_string=ustring.encode()
        print("type of new String ",type(new_string))

        bstring=b'bstring'
        new_string=bstring.decode()
        print("type of bstring",type(bstring))

        # plot data: x, y values
        #self.graphWidget.plot(hour, temperature)
        #self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

        self.graphWidget = pg.PlotWidget(
        title="Presión",
        labels={'left': 'Pressure'},
        axisItems={'bottom': TimeAxisItem(orientation='bottom')}
        )
        #self.setCentralWidget(self.graphWidget)

        self.graphWidget.setTitle("Presion vs Volumen");

        #self.graphWidget.setYRange(0,100)
        self.graphWidget.setXRange(timestamp(),timestamp()+100)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,10) for _ in range(100)]  # 100 data points
#        self.x=[]
#        self.y=[]
#        self.x.append(0.0)
#        self.y.append(0.0)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
               
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def setInitialData(self):
        self.labelPmax.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelPmax.setText(str(self.pmaxRead))

        #Read Data from PLC

        self.connectToPLC()

        pressure=readPLC.get_db_row("","","")



    def connectToPLC(self):
        t = time.time()
        print("begin: %s", %(t))
        client = snap7.client.Client()
        client.connect('192.168.0.1', 0, 1)

        db1 = make_item_db(1)
        all_data = db1._bytearray
        dbnumber=1

        size=1
        self.write_data_db(1,all_data,size)

        db1=self.get_db_row(1,0,2)
        print("db1 ",db1)

        print("end: %s", %(time.time()-t))


    def write_data_db(self,dbnumber, all_data, size):
        area = snap7.snap7types.S7AreaDB
        dbnumber = 1
        client.write_area(area, dbnumber, 0, size, all_data)

    def get_db_row(self,db, start, size):
        """
        Here you see and example of readying out a part of a DB
        Args:
            db (int): The db to use
            start (int): The index of where to start in db data
            size (int): The size of the db data to read
        """
        type_ = snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]
        data = client.db_read(db, start, type_, size)
        # print_row(data[:60])
        return data

    def openParameterWindow(self):
        app= QtWidgets.QApplication(sys.argv)
        main=Parameters()
        main.show()
        #sys.exit(app.exec_())

    def plot(self, presure, time):
        self.graphWidget.plot(presure, time)
    def update_plot_data(self):
        print("update plot data")
        #read data from the sensor connected to Arduino
#        ser = serial.Serial('/dev/pts/5',57600)
#        time.sleep(2)

#        data=[]
#        for i in range(50):
#            b=ser.readline()
#            string_n=b.decode()
#            string=string_n.rstrip()
#            flt=float(string)
#            print(flt)
#            data.append(flt)
#            time.sleep(0.1)
#        ser.close()

        #calculus of pressure
        a=48
        p=(48/1023)/((4.7-0.2)*0.018)
        p=p-0.04

        toCmH20=p*10.19716

        toCmH20=round(toCmH20,2)

        if toCmH20>self.pmaxRead:
            self.pmaxRead=toCmH20
            self.labelPmax.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
            self.labelPmax.setText(str(self.pmaxRead))

        if toCmH20>self.pmax:
           self.showAlarmMaxPressure()

        if toCmH20<self.pmin:
           self.showAlarmMinPressure()

        self.labelVolume.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
        self.labelVolume.setText(str(450))


        self.labelFreq.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
        self.labelFreq.setText(str(20))


        self.labelPeep.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelPeep.setText(str(toCmH20))

        self.labelInspEsp.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelInspEsp.setText(str(1)+":"+str(2))



        print("kPa ",p);
        print("cmH20 ",toCmH20)

        sec='%s%s'%(time.localtime().tm_min,time.localtime().tm_sec)
        print ("time: %s",sec)

        p=p+randint(0,100)

        timeNow=time.localtime()
        timeNow=time.strftime("%d/%m/%Y %H:%M:%S",timeNow)

        rightNow=int('%s%s%s'%(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec))
        print("righNow %s" %(rightNow))

        print("%s  %s" %(timeNow, p))

        #self.x = self.x[1:]  # Remove the first y element.
        self.x.append(timestamp())  # Add a new value 1 higher than the last.

        #self.y = self.y[1:]  # Remove the first
        self.y.append(p)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


    def showAlarmMaxPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet("background-color: rgb(239, 41, 41);")

    def showAlarmMinPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet("background-color: rgb(239, 41, 41);")

def closeEvent(self,event):
    print("window closed")
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
