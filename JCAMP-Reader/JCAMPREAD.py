import os
import sys
import math
import matplotlib.pyplot as plot

#filename = 'EFG.jdx'
#infile = open(filename, 'r') # Open file for reading
#line = infile.readline() # Read first line
# Read x and y coordinates from the file and store in lists
#x = []
#y = []
class extractspectra:
    def loadfile(self, filename):
        self.infile = open(filename, 'r')
        self.line = self.infile.readline()
    def findnumericdata(self):
        self.linearray = []
        self.numericline = []
        for self.line in self.infile: #Find only numberic entries and generate
            if self.line[0].isdigit():
                self.numericline.append(self.line)
        for i in range(len(self.numericline)):
            self.linearray.append(self.numericline[i].split())
    def splitxy(self):
        self.x =[]
        self.y =[]
        for a in range(len(self.linearray)):
            self.x.append(round(float(self.linearray[a][0]),3)) #Generate floating point array for X-Values(Wavenumber)
        self.yentries = self.linearray
        for a in range(len(self.yentries)):
            del self.yentries[a][0]
        for i in range(len(self.yentries)):
            self.sum=0
            for a in range(len(self.yentries[i])):
                self.sum += float(self.yentries[i][a])
            self.y.append(round(self.sum/len(self.yentries[i]),3))
        for i in range(len(self.y)):
            print self.x[i], self.y[i]
        plot.plot(self.x,self.y)
        plot.show()







file1 = "ABC.jdx"
run = extractspectra()
run.loadfile(file1)
run.findnumericdata()
run.splitxy()



    ##y.append(yaverage)
##for i in range(len(x)):
    ##print "x-Value:",x[i],"y-Average:",y[i]

#words = line.split() # Split line into words
#x.append(float(words[0]))
#y.append(float(words[1]))
#infile.close()