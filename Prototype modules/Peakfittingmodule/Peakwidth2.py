import math
import numpy as np
import matplotlib.pyplot as plt
import csv 
plt.rcParams['axes.facecolor'] = 'gray'

class calculate:
    def setup(self,xarray,yarray,xpeak,stdev):
        self.xar = xarray
        self.yar = yarray
        self.sdev=stdev
        self.difference=[]
        for i in range(len(self.xar)): 
            self.difference.append(abs(self.xar[i]-xpeak))
        self.xpeakindex=self.difference.index(min(self.difference))
        self.xpk=self.xar[self.xpeakindex]
        print self.xpk
        self.ypk=(self.yar[self.xpeakindex])
        print self.ypk
        self.interval=self.xar[10]-self.xar[9]
        print self.interval
        self.gaussarray(self.xpk,self.ypk,self.interval,self.sdev)
        self.lorentzianarray(self.xpk,self.ypk,self.interval,stdev)
        
    def gaussian(self,xcentre,ycentre,sigma,delta):
        self.deltaxpwr = (delta-xcentre)**2
        self.sigmapowr = 2*((sigma)**2)
        self.ygaus = float(1-(1-ycentre)*(math.exp(-self.deltaxpwr/self.sigmapowr)))
        return self.ygaus
    def lorentzian(self,xcentre,ycentre,whalf,delta):
        self.deltaxlor=float(delta-xcentre)
        self.ylor=float(1-(1-ycentre)*((whalf**2)/((delta-xcentre)**2+whalf**2)))
        return self.ylor
    def lorentzianarray(self,xcentre,ycentre,mininterval,whalf):
        self.xpluslor = []
        self.ypluslor=[]
        self.xminuslor= []
        self.yminuslor=[]
        self.counterlor = 0
        while  self.counterlor*0.1*mininterval <= whalf:
            self.intvlor=self.counterlor*0.1*mininterval
            self.xpluslor.append(xcentre+self.intvlor)
            self.ypluslor.append(self.lorentzian(xcentre,ycentre,whalf,xcentre+self.intvlor))
            self.xminuslor.append(xcentre-self.intvlor)
            self.yminuslor.append(self.lorentzian(xcentre,ycentre,whalf,xcentre-self.intvlor))
            self.counterlor += 1
        self.xlorentzian=[]
        self.ylorentzian=[]
        self.xminuslor.reverse()
        self.yminuslor.reverse()
        for i in range(len(self.xminuslor)-1):
            self.xlorentzian.append(self.xminuslor[i])
            self.ylorentzian.append(self.yminuslor[i])
        for i in range(len(self.xpluslor)):
            self.xlorentzian.append(self.xpluslor[i])
            self.ylorentzian.append(self.ypluslor[i])
        for i in range(len(self.xlorentzian)):
            print "xlor:",self.xlorentzian[i],"y:",self.ylorentzian[i]

    def gaussarray(self,xcentre,ycentre,mininterval,sigma):
        self.xplus = []
        self.yplus=[]
        self.xminus= []
        self.yminus=[]
        self.intval=mininterval
        self.counter = 0
        while  self.counter*0.05*self.intval <= 1.52*sigma:
            self.xplus.append(xcentre + self.counter*0.05*self.intval)
            self.yplus.append(self.gaussian(xcentre,ycentre,sigma,(xcentre+self.counter*0.05*self.intval)))
            self.xminus.append(xcentre - self.counter*0.05*self.intval)
            self.yminus.append(self.gaussian(xcentre,ycentre,sigma,(xcentre-self.counter*0.05*self.intval)))
            self.counter += 1
        self.xgaussian=[]
        self.ygaussian=[]
        self.xminus.reverse()
        self.yminus.reverse()
        for i in range(len(self.xminus)-1):
            self.xgaussian.append(self.xminus[i])
            self.ygaussian.append(self.yminus[i])
        for i in range(len(self.xplus)):
            self.xgaussian.append(self.xplus[i])
            self.ygaussian.append(self.yplus[i])

        for i in range(len(self.xgaussian)):
            print "xg:",self.xgaussian[i],"yg:",self.ygaussian[i]
            

    def returnresults(self,curve,switch):
        if curve == "gauss" and switch == "x":
            return self.xgaussian
        elif curve == "gauss" and switch == "y":
            return self.ygaussian
        elif curve == "lorentzian" and switch == "x":
            return self.xlorentzian 
        elif curve == "lorentzian" and switch == "y":
            return self.ylorentzian
        elif curve == "spectra" and switch =="y":
            return self.yar
        elif curve == "spectra" and switch =="x":
            return self.xar
        elif curve == "minima" and switch == "x":
            return self.xpk
        elif curve == "minima" and switch == "y":
            return self.ypk

class testfit:
    def findnearestx(self,xar,yar,xfit,yfit):
        self.yfit=yfit
        self.yfitindex=[]
        for i in range(len(yfit)):
            if yfit[i]==max(self.yfit):
                self.yfitindex.append(i)
        self.maxfitx1=xfit[self.yfitindex[0]]
        if len(self.yfitindex)>1:
            self.maxfitx2=xfit[self.yfitindex[1]]
        self.maxfity=max(self.yfit)
        print "maxfitx:",self.maxfitx1
        self.nearestdiff=[]
        self.nearestdiffrev=[]
        self.xar = xar[::-1]
        self.yar = yar[::-1]
        for i in range(len(self.yar)):
            self.nearestdiff.append(abs(self.xar[i]-self.maxfitx1))
        self.xindex=self.nearestdiff.index(min(self.nearestdiff))
        self.xneighbour =self.xar[self.xindex]
        self.yneighbour = self.yar[self.xindex]
        if len(self.yfitindex)>1:
                for i in range(len(self.yar)):
                    self.nearestdiffrev.append(abs(self.xar[i]-self.maxfitx2))
                self.xindexrev=self.nearestdiffrev.index(min(self.nearestdiffrev))
                self.xneighbourrev =self.xar[self.xindexrev]
                self.yneighbourrev =self.yar[self.xindexrev]
                                                            
        print "index1:",self.xindex,"index2:",self.xindexrev
        print "Closest-x:",self.xneighbour,"Closest-y:",self.yneighbour,"closrev-x:",self.xneighbourrev,"closestre-y:",self.yneighbourrev
        if self.yneighbourrev > self.yneighbour:
            self.yneigh = self.yneighbourrev
        else:
            self.yneigh = self.yneighbour
        if self.maxfity >= self.yneigh:
            print "True"
            return True
        else:
            print "False"
            return False
        
def fitminima(xminima,parameter,curve):
    if curve == "gaussian":
        param = parameter
        counter = 1
        condition = True
        while condition == True:
            param = 5*0.5*counter
            print "parameter-test",param
            abcd.setup(xwavenum,ytransmittancefract,xminima,param)
            xarray = abcd.returnresults("spectra","x")
            yarray = abcd.returnresults("spectra","y")
            xlorentz = abcd.returnresults("lorentzian","x")
            ylorentz =abcd.returnresults("lorentzian","y")
            xgauss =abcd.returnresults("gauss","x")
            ygauss =abcd.returnresults("gauss","y")
            condition = cde.findnearestx(xarray,yarray,xgauss,ygauss)
            counter += 1
        plotc(abcd.returnresults("minima","x"),abcd.returnresults("minima","y"),param,"gauss")
    elif curve == "lorentzian":
        param = parameter
        counter = 1
        condition = True
        while condition == True:
            param = 5*0.5*counter
            print "parameter-test",param
            abcd.setup(xwavenum,ytransmittancefract,xminima,param)
            xarray = abcd.returnresults("spectra","x")
            yarray = abcd.returnresults("spectra","y")
            xlorentz = abcd.returnresults("lorentzian","x")
            ylorentz =abcd.returnresults("lorentzian","y")
            xgauss =abcd.returnresults("gauss","x")
            ygauss =abcd.returnresults("gauss","y")
            condition = cde.findnearestx(xarray,yarray,xlorentz,ylorentz)
            counter += 1
        plotc(abcd.returnresults("minima","x"),abcd.returnresults("minima","y"),param,"lorentz")
    
def plotc(xcentre,ycentre,parameter,curve):
    if curve == "lorentz":
        condition = True
        xplotplus=[]
        xplotminus=[]
        yplotplus=[]
        yplotminus=[]
        counter = 0
        currentyplus = 0
        while currentyplus < 0.98:
            xplotplus.append(xcentre + counter*5)
            xplotminus.append(xcentre - counter*5)
            currentyplus = float(1-(1-ycentre)*((parameter**2)/(((xcentre+counter*5)-xcentre)**2+parameter**2)))
            yplotplus.append(currentyplus)
            yplotminus.append(currentyplus)
            counter += 1
        plt.plot(xplotminus,yplotminus,'r--',linewidth=0.5)
        plt.plot(xplotplus,yplotplus,'r--',linewidth=0.5)
    elif curve == "gauss":
        condition = True
        xplotplus=[]
        xplotminus=[]
        yplotplus=[]
        yplotminus=[]
        counter = 0
        currentyplus = 0
        while currentyplus < 0.99999:
            xplotplus.append(xcentre + counter*5)
            xplotminus.append(xcentre - counter*5)
            currentyplus = float(1-(1-ycentre)*(math.exp(-1*(((xcentre+counter*5)-xcentre)**2)/(2*(parameter**2)))))
            yplotplus.append(currentyplus)
            yplotminus.append(currentyplus)
            counter += 1
        plt.plot(xplotminus,yplotminus,'g--',linewidth=0.5)
        plt.plot(xplotplus,yplotplus,'g--',linewidth=0.5)
    #plt.show()
##    plt.plot(abcd.returnresults("spectra","x"),abcd.returnresults("spectra","y"))
##    plt.plot(abcd.returnresults("gauss","closestre-y: 0.93143471252x"),abcd.returnresults("gauss","y"))
##    plt.plot(abcd.returnresults("lorentzian","x"),abcd.returnresults("lorentzian","y"))
##    plt.show()



dataset = csv.reader(open("Tryptophansmooth.csv"), delimiter=',')
xwavenum = []
ytransmittance = []
ytransmittancefract = []
for row in dataset:
    xwavenum.append(float(row[0]))
    ytransmittance.append(float(row[1]))
for i in range(len(ytransmittance)):
    ytransmittancefract.append(((ytransmittance[i]) / (max(ytransmittance))))
dataset2 = csv.reader(open("Tryptophanminimas.csv"), delimiter=',')
xwavenummin_1 = []
ytransmittancemin_1=[]
for row in dataset2:
    xwavenummin_1.append(float(row[0]))
    ytransmittancemin_1.append(float(row[1]))
ytransmittancemin = min(ytransmittancemin_1)
xwavenummin_2=[]
ytransmittancemin_2=[]
for i in range(len(xwavenummin_1)):
    if ytransmittancemin_1[i] <= (1-((1-ytransmittancemin)/2.5)):
        xwavenummin_2.append(xwavenummin_1[i])
        ytransmittancemin_2.append(ytransmittancemin_1[i])




abcd=calculate()
cde = testfit()
for i in range(len(xwavenummin_2)):
    fitminima(xwavenummin_2[i],10,"lorentzian")
    fitminima(xwavenummin_2[i],10,"gaussian")


plt.plot(abcd.returnresults("spectra","x"),abcd.returnresults("spectra","y"),'b',linewidth=1)
plt.show()








