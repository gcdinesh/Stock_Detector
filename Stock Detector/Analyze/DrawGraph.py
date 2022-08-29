import pandas as pd
from pandas import DataFrame
from os.path import exists
from matplotlib.pylab import rcParams
from pandas_datareader import data
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
outputDf = DataFrame()
rcParams['figure.figsize'] = 20, 10
firstTime = True


class Analyzer(object):
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        self.resultDf = DataFrame()

    def readFile(self):
        filePath = "C:/Users/gcdin/Downloads/yahoo/" + self.tickerSymbol + ".csv"
        fileExists = exists(filePath)
        if(not fileExists):
            print("File does not exist. Fetching it for: " + self.tickerSymbol)
            panel_data = data.DataReader(
                self.tickerSymbol, 'yahoo', '2000-01-01', '2022-08-23')
            DataFrame(panel_data).to_csv(filePath)
        else:
            print("File Exists for: " + self.tickerSymbol)
        file = pd.read_csv(filePath)
        self.df = DataFrame(file)

    def cleanse(self):
        self.df = self.df.drop(['Open', 'High', 'Low', 'Volume'], axis=1)
        self.df = self.df.dropna()
        self.df.index = self.df['Date']

    def calculateFinally(self):
        self.resultDf[self.tickerSymbol] = self.df['Close']

    def writeToFile(self):
        global outputDf
        global firstTime
        if(firstTime):
            outputDf = DataFrame(self.resultDf)
            firstTime = False
        else:
            outputDf[self.tickerSymbol] = self.resultDf

    def printdf(self):
        print(outputDf)


tickerSymbols = ["BAJFINANCE.NS", "ULTRACEMCO.NS", "SKFINDIA.NS", "ASIANPAINT.NS",
                 "TCS.NS", "HINDUNILVR.NS", "AIAENG.NS", "TITAN.NS", "POLYCAB.NS",
                 "HDFC.NS", "ASTRAL.NS", "KOTAKBANK.NS",
                 "BATAINDIA.NS", "PVR.NS", "COLPAL.NS", "INFY.NS",
                 "HDFCBANK.NS", "HCLTECH.NS", "KPIGREEN.NS", "DABUR.NS",
                 "KANSAINER.NS", "TATAPOWER.NS", "DEVYANI.NS", "^NSEI"]

for i in tickerSymbols:
    analyze = Analyzer(i)
    analyze.readFile()
    analyze.cleanse()
    analyze.calculateFinally()
    analyze.writeToFile()
    # analyze.printdf()

outputDf = outputDf.fillna(0)
niftyDf = DataFrame(outputDf['^NSEI'])
niftyDf = niftyDf[(niftyDf.T != 0).any()]  # removing 0 values
outputDf = outputDf.drop(['^NSEI'], axis=1)
outputDf = outputDf.sum(axis=1)

# outputDf = (outputDf-outputDf.min())/(outputDf.max()-outputDf.min())
# niftyDf = (niftyDf-niftyDf.min())/(niftyDf.max()-niftyDf.min())


# plt.plot(outputDf)
# plt.plot(niftyDf)
# plt.legend(["All", "Nifty"], loc="lower right")

outputDf.to_csv("graph.csv")
