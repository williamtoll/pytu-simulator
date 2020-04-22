# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from decimal import Decimal
import sys
import sqlite3

class Parameters(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)

        #self.createDatabase()

        #self.createData()


        #Load the UI Page
        uic.loadUi('parameters.ui', self)
        self.pushButton.pressed.connect(self.on_button_clicked)

        self.poblateFormWithData()



    def on_button_clicked(self):
      print("Marcha "+self.txtMarcha.text())
      self.txtMarcha.setText('xxxx')
      alert = QMessageBox()
      alert.setText('Button clicked')
      alert.exec_()

    def alert(self, message):
      alert = QMessageBox.warning(self, "Warning", message)

    def createDatabase(self):
        conn = sqlite3.connect('pytu.db')

        c = conn.cursor()

        # Create table
    #    c.execute('''CREATE TABLE parameters
    #                 (key text, value text, comment text)''')

        # Insert a row of data
        c.execute("INSERT INTO parameters VALUES ('marcha','DB7','Boton de marcha')")

        t = ('marcha',)
        c.execute('SELECT * FROM parameters WHERE key=?', t)
        print (c.fetchone())



        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    def createData(self):
        conn = sqlite3.connect('pytu.db')

        c = conn.cursor()
        c.execute("delete from parameters")

        # Insert a row of data
        c.execute("INSERT INTO parameters VALUES ('marcha','DB7','Boton de marcha')")
        c.execute("INSERT INTO parameters VALUES ('parada','DB8','Boton de parada')")
        c.execute("INSERT INTO parameters VALUES ('presion','DB9','Sensor de Presion')")
        c.execute("INSERT INTO parameters VALUES ('volumen','DB10','Sensor de volumen')")
        c.execute("INSERT INTO parameters VALUES ('flujo','DB11','Sensor de flujo')")
        c.execute("INSERT INTO parameters VALUES ('tiempo1','DB12','Tiempo1')")
        c.execute("INSERT INTO parameters VALUES ('tiempo2','DB13','Tiempo2')")


        #parameter
#        t = ('marcha',)
#        c.execute('SELECT * FROM parameters WHERE key=?',t)
#        print (c.fetchone())

        #fetchall
        c.execute('SELECT * FROM parameters WHERE 1=1')
        print (c.fetchall())



        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


    def poblateFormWithData(self):
        conn=sqlite3.connect("pytu.db")
        c=conn.cursor()

        c.execute('SELECT * FROM parameters WHERE 1=1')
        print (c.fetchall())

        clave='marcha'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})

        res=c.fetchone()
        print("result: ",res)
        print(self.txtMarcha.text())
        if res is not None:
            self.txtMarcha.setText(''+res[0])


        clave='parada'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtParada.text())
        if res is not None:
            self.txtParada.setText(''+res[0])

        clave='presion'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtPresion.text())
        if res is not None:
            self.txtPresion.setText(''+res[0])

        clave='volumen'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtMarcha.text())
        if res is not None:
            self.txtVolumen.setText(''+res[0])

        clave='flujo'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtFlujo.text())
        if res is not None:
            self.txtMarcha.setText(''+res[0])

        clave='tiempo1'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtTiempo1.text())
        if res is not None:
            self.txtTiempo1.setText(''+res[0])

        clave='tiempo2'
        c.execute("SELECT value from parameters where key=:clave",{"clave":clave})
        print(c.fetchone())
        res=c.fetchone()
        print(self.txtTiempo2.text())
        if res is not None:
            self.txtTiempo2.setText(''+res[0])





def main():
    app= QtWidgets.QApplication(sys.argv)
    main=Parameters()
    main.show()
    sys.exit(app.exec_())





if __name__ == '__main__':
   main()
