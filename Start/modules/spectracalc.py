import csv
import math


class spectrafrominf:
    'calculates the intensity vs. wavenumber FT-IR spectra from the raw inteferrogram'
    'dependencies required in main script: math and csv'
    'Usage: class.setup(csvfilepath)'

    # 1 Loads data from csv file and stores as x and y float arrays
    def __dataload__(self, file, dlm):
        self.dataset = csv.reader(open(file), delimiter=dlm)
        self.xshift = []
        self.yintensity = []
        for row in self.dataset:
            self.xshift.append(float(row[0]))
            self.yintensity.append(float(row[1]))

    def __testdataload__(self):
        for i in range(len(self.xshift)):
            print "shift(cm):|%s|                             amplitude:|%s|" % (self.xshift[i], self.yintensity[i])
            # 2 Calculation of the resolution in 1/cm and sampling interval cm of the instrument

    def __spectraparameters__(self):
        self.sampint = 0.00006328
        ##        self.resolution = float(1/ ((self.sampint)*len(self.xshift)))
        self.resolution = 16.0

    def __testspectraparameters__(self):
        print ""
        print "Sampling interval (cm):", self.sampint, " ", "Resolution (1/cm):", self.resolution

    # 3 Triangular Apodization correction function for the raw inteferrogram data
    def __apodiseme__(self):
        self.maxval = 1 / (self.resolution)
        self.apodise = []
        self.apodiseI = []
        for i in range(len(self.yintensity)):
            self.apodise.append(0.5 * (1 + math.cos((math.pi * (self.xshift[i])) / self.maxval)))
        for ii in range(len(self.apodise)):
            self.apodiseI.append((self.yintensity[ii]) * (self.apodise[ii]))

    def __testapodiseme__(self):
        for i in range(len(self.xshift) - 900):
            print "shift(cm):|%s|            Original amplitude:|%s|              Apodisedamplitude:|%s|" % (
                self.xshift[i], self.yintensity[i], self.apodiseI[i])

            # 4 The fourier transform functions for calculating the final spectra

    def __setwaverange__(self, start, finish, res):
        'setup of waverange to be tested in DRFT of inteferrogram'
        self.waverg = []
        for i in range(int(start), int(finish), int((res))):
            self.waverg.append(i)

            #  for i in range(int(self.rge)+1):
            #    self.waverg.append(self.current + int(res))
            #    self.current = self.current + int(res)

    def __setwaverangetest__(self):
        for i in range(len(self.waverg)):
            print self.waverg[i]

    def wavenumberintensity(self, testwave):
        self.currentintensity = self.apodiseI[0]
        self.adjusted = 0
        for i in range(1, len(self.xshift)):
            self.test = (float(self.apodiseI[i])) * (math.cos((2 * math.pi) * testwave * self.xshift[i]))
            self.currentintensity += (float(self.apodiseI[i])) * (math.cos((2 * math.pi) * testwave * self.xshift[i]))
            self.adjusted = ((self.currentintensity - self.apodiseI[0]) / (self.apodiseI[0]))


            # print self.adjusted
        return self.adjusted

    def __calculatespectra__(self):
        self.transm = []
        self.perctransm = []
        self.perctransminv = []
        self.mintrsm = []
        ##self.smallesty=min(self.wavenumberintensity)
        for i in range(len(self.waverg)):
            if self.wavenumberintensity(self.waverg[i]) != 0:
                self.transm.append(self.wavenumberintensity(self.waverg[i]))
                print self.waverg[i], " ", self.transm[i]
            else:
                self.transm.append(0.0)
                print self.waverg[i], " ", self.transm[i]
        for i in range(len(self.transm)):
            self.perctransm.append((self.transm[i] - min(self.transm)) / (max(self.transm) - min(self.transm)))
            self.perctransminv.append(1 - (self.transm[i] / max(self.transm)))

            ##    def __removebounds__(self, x, y):
            ##        self.yadjust = list(y)
            ##        self.xadjust = list(x)
            ##        for i in range(len(y)):
            ##            if y[i] == 0:
            ##                del self.yadjust[i]
            ##                del self.xadjust[i]




            # Initiation method for entire class ans test functions

    def setup(self, filename, delimiter):
        self.__dataload__(filename, delimiter)
        self.__testdataload__()
        self.__spectraparameters__()
        self.__testspectraparameters__()
        self.__apodiseme__()
        self.__testapodiseme__()
        self.__setwaverange__(100, 4200, self.resolution)
        self.__setwaverangetest__()
        self.__calculatespectra__()
        ##        self.__removebounds__(self.waverg, self.perctransm)
        return

    # Retrieving values after setup
    def returnvalinf(self, a):
        'usage: returnvalinf(x or y or Ia) for shift vs original and shift vs apodised'
        if a == 'x':
            return self.xshift
        elif a == 'y':
            return self.yintensity
        elif a == 'Ia':
            return self.apodiseI

    def returnvalspec(self, a):
        'usage: returnvalinf(x or y or Ia) for shift vs original and shift vs apodised'
        if a == 'x':
            return self.waverg
        elif a == 'y':
            return self.transm
        elif a == 'yadjusted':
            return self.perctransm
        elif a == 'xadjusted':
            return self.waverg

    def datawrite(self, name, dlm):
        self.fileout = name
        self.fileoutcsv = open(self.fileout, "wb")
        writer = csv.writer(self.fileoutcsv)
        joinedlist = []
        for i in range(self.kval):
            joinedlist.append([self.waverg[i], self.transm[i]])
            writer.writerow(joinedlist[i])
        self.fileoutcsv.close()


class inffromspectra:
    # 1 Importing spectra data from CSV
    def __dataload__(self, file, dlm):
        self.dataset = csv.reader(open(file), delimiter=dlm)
        self.xwavenum = []
        self.ytransmittance = []
        self.ytransmittancefract = []
        self.sumwave = 0
        self.sumtrans = 0
        for row in self.dataset:
            self.xwavenum.append(float(row[0]))
            self.ytransmittance.append(float(row[1]))
        for i in range(len(self.ytransmittance)):
            self.ytransmittancefract.append((self.ytransmittance[i]) / (max(self.ytransmittance)))
        for i in range(len(self.xwavenum)):
            self.sumwave = +self.xwavenum[i]
            self.sumtrans = +self.ytransmittancefract[i]

    def __testdataload__(self):
        for i in range(len(self.xwavenum)):
            print "wavenumber(1/cm):|%s|                             Reltranmittance:|%s|" % (
                self.xwavenum[i], self.ytransmittancefract[i])

            # 2 Calculation of sampling interval(h as cm) resolution(1/cm) and maximum retardation and no of datapoints(kvalues)

    def __spectraparameters__(self):
        ##        self.res = (self.xwavenum[1]-self.xwavenum[0])*2
        self.res = 16.0
        self.maxret = float(1 / (self.res))
        self.sampintv = 0.00006328

        self.kval = int((self.maxret) / (self.sampintv))
        self.ytransmmax = float(sum(self.ytransmittance))

    def __testspectraparameters__(self):
        print ""
        print "Resolution(1/cm):", self.res, " ", "Maximum retardation:", self.maxret, " ", "Sampling interval:", self.sampintv, " ", "No of data points:", self.kval

    # 3 Spectracalculations
    def __calculateinf__(self):
        self.testshift = []
        self.finalamplitude = []
        for i in range(0, self.kval + 1):
            self.testshift.append(i * self.sampintv)
            self.finalamplitude.append(self.__shiftamplitude__(self.testshift[i]))

    def __shiftamplitude__(self, shift):
        self.sumamplitude = 0.0
        if shift == 0:
            for a in range(len(self.xwavenum)):
                self.sumamplitude += (self.ytransmittancefract[a])
        elif shift != 0:
            for b in range(len(self.xwavenum)):
                self.sumamplitude += (self.ytransmittance[b]) * math.cos((2 * (math.pi)) * (self.xwavenum[b]) * (shift))
        return self.sumamplitude

    def __testspectracalc__(self):
        for i in range(self.kval):
            print "shift(1/cm):", self.testshift[i], "Amplitude:", self.finalamplitude[i]


            # 4 Return values

    def returnvalspec(self, a):
        if a == 'xs':
            return self.testshift
        elif a == 'ya':
            return self.finalamplitude
        elif a == 'xw':
            return self.xwavenum
        elif a == 'yt':
            return self.ytransmittance
        else:
            print "Please provide one of the following valid arguments: \'xs\' -> shifts, \'ya\'->amplitudes, \'xw\'->wavenumbers, \'yt\'-> transmittance\'s"

            # 5 Write results to csv

    def datawrite(self, name, dlm, x, y):
        self.fileout = name
        self.fileoutcsv = open(self.fileout, "wb")
        writer = csv.writer(self.fileoutcsv)
        joinedlist = []
        for i in range(self.kval):
            joinedlist.append([self.testshift[i], self.finalamplitude[i]])
            writer.writerow(joinedlist[i])
        self.fileoutcsv.close()

    # Setup Function

    def setup(self, name, delimiter):
        self.__dataload__(name, delimiter)
        self.__testdataload__()
        self.__spectraparameters__()
        self.__spectraparameters__()
        self.__testspectraparameters__()
        self.__calculateinf__()
