import csv
import sys

import math


class calculate:
    def dataloadfile(self, file, dlm):
        self.xwave = []
        self.yintensity = []
        self.yfract = []
        self.dataset = csv.reader(open(file), delimiter=dlm)
        for row in self.dataset:
            self.xwave.append(float(row[0]))
            self.yintensity.append(float(row[1]))
        for i in range(len(self.yintensity)):
            self.yfract.append(self.yintensity[i] / max(self.yintensity))
            print "Wavenuber:", self.xwave[i], "Rel. Intensity:", self.yfract[i]

    def dataloadapp(self, x, y):
        self.xin = x
        self.yin = y
        self.xwave = []
        self.yintensity = []
        self.yfract = []
        for a in range(len(self.xin)):
            self.xwave.append(self.xin[a])
            self.yintensity.append(self.yin[a])
        for i in range(len(self.yintensity)):
            self.yfract.append(self.yintensity[i] / max(self.yintensity))
            print "Wavenuber:", self.xwave[i], "Rel. Intensity:", self.yfract[i]

    def differential(self):
        self.dydx = []
        for i in range(len(self.xwave)):
            if i == 0:
                self.dydx.append(0.0)
            else:
                self.dydx.append(
                    ((self.yfract[i] - self.yfract[int(i - 1)]) / ((self.xwave[i]) - self.xwave[int(i - 1)])))

    def detectminima(self):
        self.yminima = []
        self.yminimax = []
        for i in range((len(self.xwave))):
            if i >= 1:
                if (self.dydx[i - 1]) <= 0 < (self.dydx[i]):
                    self.yminima.append(self.yfract[i - 1])
                    self.yminimax.append(self.xwave[i - 1])
        for i in range(len(self.yminima)):
            print "Wavenuber:", self.yminimax[i]

    def addcutoff(self, ycutoff):
        self.minimaopty = []
        self.minimaoptx = []
        for i in range(len(self.yminima)):
            if self.yminima[i] < float(ycutoff):
                self.minimaopty.append(self.yminima[i])
                self.minimaoptx.append(self.yminimax[i])

    def returnvalues(self, val):
        if val == "xval":
            return self.xwave
        elif val == "yval":
            return self.yfract
        elif val == "xmin":
            return self.yminimax
        elif val == "ymin":
            return self.yminima
