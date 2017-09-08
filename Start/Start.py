import sys
import csv
from modules import spectracalc
from PyQt4.QtGui import *
from modules import peakdetecttmp
from modules.MainWindowGui import *



class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.peakcalc = peakdetecttmp.calculate()  # local instance of the peakdetection module
        ##Event Bindings
        ##1-> Event Bindings for peak calculation tab
        QtCore.QObject.connect(self.checkBoxinf_1, QtCore.SIGNAL("clicked(bool)"), self.openButton_1.setEnabled)
        QtCore.QObject.connect(self.checkBoxinf_1, QtCore.SIGNAL("clicked(bool)"), self.testcheckboxa)
        QtCore.QObject.connect(self.checkBoxspectra_1, QtCore.SIGNAL("clicked(bool)"), self.openButton_1.setEnabled)
        QtCore.QObject.connect(self.checkBoxspectra_1, QtCore.SIGNAL("clicked(bool)"), self.testcheckboxb)
        QtCore.QObject.connect(self.openButton_1, QtCore.SIGNAL("clicked()"), self.getfile)
        QtCore.QObject.connect(self.calculateButton_1, QtCore.SIGNAL("clicked()"), self.importspectra)
        QtCore.QObject.connect(self.saveButton_1, QtCore.SIGNAL("clicked()"), self.savefiledialog)

        ##2-> Event Bindings for peak picking tab
        QtCore.QObject.connect(self.pushButtonImport_2, QtCore.SIGNAL("clicked()"), self.importdata_2)
        QtCore.QObject.connect(self.pushButtonReset_2, QtCore.SIGNAL("clicked()"), self.importdata_2)
        QtCore.QObject.connect(self.pushButtonSave_2, QtCore.SIGNAL("clicked()"), self.saveresultdialog_2)

    ##Event Functions
    ##1->Functions associated with peak calculation tab
    # Checkbox control
    def testcheckboxa(self):
        self.checkBoxspectra_1.setChecked(False)
        self.checkboxstatus = 'inf'
        self.openButton_1.setEnabled(True)
        print self.checkboxstatus

    def testcheckboxb(self):
        self.checkBoxinf_1.setChecked(False)
        self.checkboxstatus = 'spec'
        self.openButton_1.setEnabled(True)
        print self.checkboxstatus

        # Open file dialog

    def getfile(self):
        self.calculateButton_1.setEnabled(True)
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '\\', "csv (*.csv *.CSV)")
        # Import spectra and calculate

    def setdelimiter(self):
        if self.radioButtoncomma_1.isChecked():
            self.delimiter = ","
        elif self.radioButtonspace_1.isChecked():
            self.delimiter = " "
        elif self.radioButtoncolon_1.isChecked():
            self.delimiter = ":"

    def importspectra(self):
        self.setdelimiter()
        self.spect = spectracalc.spectrafrominf()
        self.inf = spectracalc.inffromspectra()
        self.radioButtonFrmclc_2.setEnabled(True)
        if self.checkBoxspectra_1.isChecked():
            self.saveButton_1.setEnabled(True)
            # self.radioButtonFrmclc_2.setEnabled(True)
            self.name = self.fname
            print self.name
            self.spect.setup(self.name, self.delimiter)
            self.xsp = self.spect.returnvalspec('x')
            self.xdata = self.spect.returnvalspec('x')
            self.ysp = self.spect.returnvalspec('y')
            self.ydata = self.spect.returnvalspec('yadjusted')
            self.xinf = self.spect.returnvalinf('x')
            self.yinf = self.spect.returnvalinf('Ia')
            self.plotcurves_1(self.xinf, self.yinf, self.xsp, self.ysp, "Shift(cm)", "Relative Intensity",
                              "Wavenumber(1/cm)", "Relative Intensity")
        if self.checkBoxinf_1.isChecked():
            self.saveButton_1.setEnabled(True)
            self.name = self.fname
            # self.radioButtonFrmclc_2.setEnabled(False)
            print self.name
            self.inf.setup(self.name, self.delimiter)
            self.xsp = self.inf.returnvalspec('xw')
            self.ysp = self.inf.returnvalspec('yt')
            self.xinf = self.inf.returnvalspec('xs')
            self.xdata = self.inf.returnvalspec('xs')
            self.ydata = self.inf.returnvalspec('ya')
            self.yinf = self.inf.returnvalspec('ya')
            self.plotcurves_1(self.xsp, self.ysp, self.xinf, self.yinf, "Wavenumber(1/cm)", "Relative Intensity",
                              "Shift(cm)", "Relative Intensity")
            # Save file dialog

    def savefiledialog(self):
        self.sfname = QFileDialog.getSaveFileName(self, 'Save file', '\\', "csv (*.csv *.CSV)")
        if self.sfname:
            self.setdelimiter
            self.savefile(self.sfname, self.delimiter)

    def savefile(self, name, dlm):
        if self.checkBoxspectra_1.isChecked():
            self.datawrite(name, dlm)
        if self.checkBoxinf_1.isChecked():
            self.datawrite(name, dlm)

    def datawrite(self, name, dlm):
        self.fileout = name
        self.fileoutcsv = open(self.fileout, "wb")
        writer = csv.writer(self.fileoutcsv)
        joinedlist = []
        for i in range(len(self.xdata)):
            joinedlist.append([self.xdata[i], self.ydata[i]])
            writer.writerow(joinedlist[i])
        self.fileoutcsv.close()
        # Curve plotting functions

    def plotcurves_1(self, x, y, x2, y2, xlabel1, ylabel1, xlabel2, ylabel2):
        self.Plot1_1.show()
        self.Plot1_1.setLabel('left', ylabel1)
        self.Plot1_1.setLabel('bottom', xlabel1)
        if self.checkBoxinf_1.isChecked():
            self.Plot1_1.invertX(True)
            self.Plot2_1.invertX(False)
        self.Plot2_1.show()
        self.Plot2_1.setLabel('left', ylabel2)
        self.Plot2_1.setLabel('bottom', xlabel2)
        if self.checkBoxspectra_1.isChecked():
            self.Plot2_1.invertX(True)
            self.Plot1_1.invertX(False)
        self.Plot1_1.clear()
        self.Plot1_1.showGrid(x=True, y=True)
        self.Plot1_1.plot(x, y, pen='b')
        self.Plot2_1.clear()
        self.Plot2_1.showGrid(x=True, y=True)
        self.Plot2_1.plot(x2, y2, pen='r')

        ##2->Functions associated with peak picking tab
        # Data importation

    def getfile_2(self):
        self.fname_2 = QFileDialog.getOpenFileName(self, 'Open file', '\\', "csv (*.csv *.CSV)")
        self.peakcalc.dataloadfile(self.fname_2, ',')

    def importdata_2(self):
        # Check datasource
        if self.radioButtonFrmclc_2.isChecked():
            if self.checkBoxinf_1.isChecked():
                self.peakcalc.dataloadfile(self.fname, self.delimiter)
                self.peakcalc.differential()
                self.peakcalc.detectminima()
                self.localx = self.peakcalc.returnvalues("xmin")  # local array to be updated when plot is clicked
                self.localy = self.peakcalc.returnvalues("ymin")
                self.plotcurves_2(self.peakcalc.returnvalues("xval"), self.peakcalc.returnvalues("yval"), self.localx,
                                  self.localy)
            else:
                self.peakcalc.dataloadapp(self.xsp, self.ysp)
                self.peakcalc.differential()
                self.peakcalc.detectminima()
                self.localx = self.peakcalc.returnvalues("xmin")  # local array to be updated when plot is clicked
                self.localy = self.peakcalc.returnvalues("ymin")
                self.plotcurves_2(self.peakcalc.returnvalues("xval"), self.peakcalc.returnvalues("yval"), self.localx,
                                  self.localy)
        elif self.radioButtonFrmcsv_2.isChecked():
            self.getfile_2()
            self.peakcalc.differential()
            self.peakcalc.detectminima()
            self.localx = self.peakcalc.returnvalues("xmin")  # local array to be updated when plot is clicked
            self.localy = self.peakcalc.returnvalues("ymin")
            self.plotcurves_2(self.peakcalc.returnvalues("xval"), self.peakcalc.returnvalues("yval"), self.localx,
                              self.localy)
        #Curve plotting functions for the peak-picking tab
    def plotcurves_2(self, x, y, xmin, ymin):
        self.Plot1_2.setMouseEnabled(x=True, y=True)
        self.Plot1_2.setLabel('left', "Relative Intensity")
        self.Plot1_2.setLabel('bottom', "Wavenumber(1/cm)")
        self.Plot1_2.showGrid(x=True, y=True)
        self.Plot1_2.invertX(True)
        self.Plot1_2.show()
        self.Plot1_2.clear()
        self.Plot1_2.plot(x, y, pen='r')
        self.Plot1_2.plot(xmin, ymin, pen=None, symbol='+', symbolSize=5, clickable=True)
        self.proxy = pg.SignalProxy(self.Plot1_2.scene().sigMouseClicked, rateLimit=60, slot=self.ClickPoint) #Event listner for the mouseclick event on data-points
        # self.Plot1_2.scene().sigMouseClicked.connect(self.addPoint)

    def ClickPoint(self, event):
        self.position = event[0].pos().x() #Returns Mouseclick position terms of plot x,y coordinates
        self.positiony = event[0].pos().y()
        self.locallocalx = self.localx
        self.locallocaly = self.localy
        self.tempremovex = None
        self.tempremovey = None
        print "clicked", self.position
        self.tabWidget.setTabEnabled(2, True)
        self.pushButtonSave_2.setEnabled(True)
        for i in range(len(self.localx)):
            if ((self.localx[i] + 10) >= self.position >= (self.localx[i] - 10)) and (
                            (self.localy[i] + 0.05) >= self.positiony >= (self.localy[i] - 0.05)):
                del self.localx[i]
                del self.localy[i]
                print "THIS VALUE", self.localx[i - 1]
                break
        for i in range(len(self.localx)):
            print "X-coord", self.localx[i], "y-coord", self.localy[i]
        if self.radioButtonFrmclc_2.isChecked():
            self.plotcurves_2(self.peakcalc.returnvalues("xval"), self.peakcalc.returnvalues("yval"), self.localx,
                              self.localy)
        elif self.radioButtonFrmcsv_2.isChecked():
            self.plotcurves_2(self.peakcalc.returnvalues("xval"), self.peakcalc.returnvalues("yval"), self.localx,
                              self.localy)
        self.Resultupdate()

    ##Functions associated with the results tab
    def Resultupdate(self):
        self.scene = QGraphicsScene(self)
        self.pixmap = QtGui.QPixmap()
        self.pixmap.load("modules/Zones.jpg")
        self.scene.addPixmap(self.pixmap)
        self.graphicsView.setScene(self.scene)
        self.tableWidget.setRowCount(len(self.localx))
        for i in range(len(self.localx)):
            self.tableWidget.setItem(i, 0, QtGui.QTableWidgetItem(str(self.localx[i])))
            self.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(str(round((1 - self.localy[i]), 2))))
            self.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(self.Zone(self.localx[i])))

    def Zone(self, wavenumber):
        self.zone = None
        if wavenumber < 1450:
            self.zone = "Fingerprint Region"
        elif 1450 <= wavenumber < 1680:
            self.zone = "Zone 5"
            if wavenumber < 1680:
                self.zone = "Zone 4 or 5"
        elif 1680 <= wavenumber < 1850:
            self.zone = "Zone 4"
        elif 2000 <= wavenumber < 2300:
            self.zone = "Zone 3"
        elif 2700 <= wavenumber < 3200:
            self.zone = "Zone 2"
        elif 3200 <= wavenumber < 3700:
            self.zone = "Zone 1"
        else:
            self.zone = "Not Assigned"
        return self.zone

    def saveresultdialog_2(self):
        self.sfname_2 = QFileDialog.getSaveFileName(self, 'Save file', '\\', "csv (*.csv *.CSV)")
        if self.sfname_2:
            self.savefile_2(self.sfname_2, ',')

    def savefile_2(self, name, dlm):
            self.datawrite_2(name, dlm)

    def datawrite_2(self, name, dlm):
        self.fileout_2 = name
        self.fileoutcsv_2 = open(self.fileout_2, "wb")
        writer = csv.writer(self.fileoutcsv_2)
        joinedlist_2 = []
        for i in range(len(self.localx)):
            joinedlist_2.append([self.localx[i], self.localy[i], self.Zone(self.localx[i])])
            writer.writerow(joinedlist_2[i])
        self.fileoutcsv_2.close()




app = QtGui.QApplication(sys.argv)
dw = MainWindow()
dw.show()
sys.exit(app.exec_())
