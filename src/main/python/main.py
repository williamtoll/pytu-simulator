from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import serial
import time
from random import randint
from utils import TimeAxisItem, timestamp
import snap7
from snap7 import *


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


        self.pushButtonResetAlarms.pressed.connect(self.resetAlarms)

        self.pushButtonMarcha.pressed.connect(self.startPLC)

        self.pushButtonParada.pressed.connect(self.stopPLC)

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

        self.graphWidget.setYRange(0,100)
        self.graphWidget.setXRange(timestamp(),timestamp()+100)

        self.x = []  # 100 time points
#        self.y = [randint(0,10) for _ in range(100)]  # 100 data points
        self.y=[]

        self.x.append(timestamp())
        self.y.append(0)

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)



        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def setInitialData(self):
        self.labelPmax.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelPmax.setText(str(self.pmaxRead))



    def startPLC(self):
        print("startPLC")
        plc = snap7.client.Client()
        plc.connect('192.168.0.1', 0, 1)


        reading = plc.db_read(3, 0, 1)    # read 1 byte from db 3 staring from byte 0
        print(reading)


        str="10"
        data=bytearray(str,'utf-8')
#        reading=plc.as_db_read(3,0,1)
#        print(reading)


        plc.db_write(3,0,data)

#        reading = plc.db_read(3, 0, 1)    # read 1 byte from db 3 staring from byte 0
#        print(reading)
#        reading =reading.rstrip()
#        print(reading)


    def stopPLC(self):
        print("startPLC")
        plc = snap7.client.Client()
        plc.connect('192.168.0.1', 0, 1)


        reading = plc.db_read(3, 1, 1)    # read 1 byte from db 3 staring from byte 0
        print(reading)


        str="20"
        data=bytearray(str,'utf-8')
        plc.db_write(3,0,data)



    def resetAlarms(self):
        self.disableAlarmMaxPressure()
        self.disableAlarmMinPressure()
    def plot(self, presure, time):
        self.graphWidget.plot(presure, time)
    def update_plot_data(self):
        print("update plot data")
        #read data from the sensor connected to Arduino
        ser = serial.Serial('/dev/ttyACM0',57600)
        plc = snap7.client.Client()
        plc.connect('192.168.0.1', 0, 1)
        print(plc.get_connected)
        #time.sleep(3)

        b=ser.readline()
        string_n=b.decode()
        string=string_n.rstrip()
        print(string)
        flt=int(string)
        print(flt)
        #time.sleep(0.1)
        ser.close()

        #calculus of pressure
        a=flt
#        a = randint(10,100)
        p=(a/1023)/((4.7-0.2)*0.018)
        p=p-0.04

        toCmH20=p*10.19716

        toCmH20=round(toCmH20,2)


        for_plc_int=str(flt)
        print("for plc %s" %(for_plc_int))
        data_int=bytearray(for_plc_int,'utf-8')
        print("for plc int")
        print(data_int)

        for_plc_real=str(toCmH20)
        print("for plc real %s" %(for_plc_real))
        data_real=bytearray(for_plc_real,'utf-8')

#        print(data.rstrip())

#        print("db3")
#        print(plc.as_db_get(3))

#        type_ = snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte]
#        db3_data = plc.db_read(3, 22, type_, 2)
#        plc.set_connection_params

#        #plc.db_write(3,2,22,data)
#        area = snap7.snap7types.S7AreaDB
#        plc.write_area(area,3,22,data)


#        reading=plc.as_db_read(3,22,2)
#        snap7.util.set_int(reading,0,flt)
#        plc.as_db_write(3,22,reading)


        #plc.disconnect()

        if toCmH20>self.pmaxRead:
            self.pmaxRead=toCmH20
            self.labelPmax.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
            self.labelPmax.setText(str(self.pmaxRead))


        if toCmH20>self.pmax:
           self.showAlarmMaxPressure()
        else:
           self.disableAlarmMaxPressure()

        if toCmH20<self.pmin:
           self.showAlarmMinPressure()
        else:
           self.disableAlarmMinPressure()

        self.labelVolume.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
        self.labelVolume.setText(str(450))


        self.labelFreq.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87; text-align:center")
        self.labelFreq.setText(str(20))


        self.labelPeep.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelPeep.setText(str(toCmH20))

        self.labelInspEsp.setStyleSheet("background-color: rgb(186, 189, 182); font-size:36pt; font-weight:600; color:#204a87;")
        self.labelInspEsp.setText(str(1)+":"+str(2))




        reading=plc.db_read(3,18,4)
        print("formate float value")
        print(reading)
        snap7.util.set_real(reading,0,toCmH20)
        print(reading)
        plc.db_write(3,18,reading)

        print("kPa ",p);
        print("cmH20 ",toCmH20)

        sec='%s%s'%(time.localtime().tm_min,time.localtime().tm_sec)
        print ("time: %s",sec)

#        p=p+randint(0,100)

        timeNow=time.localtime()
        timeNow=time.strftime("%d/%m/%Y %H:%M:%S",timeNow)

        rightNow=int('%s%s%s'%(time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec))
        print("righNow %s" %(rightNow))

        print("%s  %s" %(timeNow, p))

        self.x = self.x[1:]  # Remove the first element.
        #self.x= timestamp()
        print("timestamp: %s" %(timestamp()))
        self.x.append(timestamp())  # Add a new value 1 higher than the last.

        print("time values")
        print(self.x)

        self.y = self.y[1:]  # Remove the first
        self.y.append(toCmH20)  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


    def showAlarmMaxPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet(red)
        self.labelAlarma.setStyleSheet(" font-size:18pt; font-weight:600;")
        self.labelAlarma.setText("PRESION FUERA DE RANGO MAX")
        self.playSound();

    def showAlarmMinPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet(red)
        self.labelAlarma.setStyleSheet(" font-size:18pt; font-weight:600;")
        self.labelAlarma.setText("PRESION FUERA DE RANGO MIN")
        self.playSound();

    def disableAlarmMaxPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet(green)
        self.labelAlarma.setStyleSheet(" font-size:18pt; font-weight:600;")
        self.labelAlarma.setText("NORMAL")

    def disableAlarmMinPressure(self):
        green="background-color: rgb(115, 210, 22);"
        red="background-color: rgb(239, 41, 41);"
        self.groupBoxAlarm.setStyleSheet(green)
        self.labelAlarma.setStyleSheet(" font-size:18pt; font-weight:600;")
        self.labelAlarma.setText("NORMAL")


    def playSound(self):
        duration = 1  # seconds
        freq = 300  # Hz
        #os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        #os.system('spd-say "Error"')

def closeEvent(self,event):
    print("window closed")
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
