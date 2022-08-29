import pandas as pd
from pandas import DataFrame
from os.path import exists
from pandas_datareader import data
import re

pd.set_option('display.max_columns', None)
outputDf = DataFrame()
firstTime = True


class Analyzer(object):
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        self.resultDf = DataFrame()

    def readFile(self):
        filePath = "C:/Users/gcdin/Downloads/screener/" + self.tickerSymbol + ".txt"
        fileExists = exists(filePath)
        if(not fileExists):
            print("File does not exist. Fetching it for: " + self.tickerSymbol)
            # panel_data = data.DataReader(
            #     self.tickerSymbol, 'yahoo', '2000-01-01', '2022-08-23')
            # DataFrame(panel_data).to_csv(filePath)
        else:
            print("File Exists for: " + self.tickerSymbol)
        with open(filePath) as f:
            self.lines = f.readlines()

    def getPercentageDetails(self):
        for line in self.lines:
            fmtLines = re.sub(r"\[[^\]]*\]", "", str(line)
                              ).replace('\n', '. ').lower().split('. ')
            for fmtLine in fmtLines:
                if(str(fmtLine).find('lead') >= 0):
                    print(fmtLine.strip(' '))

    def writeToFile(self):
        global outputDf
        outputDf = outputDf.append(self.resultDf, ignore_index=True)

    def printdf(self):
        print(outputDf)


tickerSymbols = ["BAJFINANCE", "ULTRACEMCO.NS", "SKFINDIA.NS", "ASIANPAINT.NS",
                 "TCS.NS", "HINDUNILVR.NS", "AIAENG.NS", "TITAN.NS", "POLYCAB.NS",
                 "HDFC.NS", "ASTRAL.NS", "KOTAKBANK.NS",
                 "BATAINDIA.NS", "PVR.NS", "COLPAL.NS", "INFY.NS",
                 "HDFCBANK.NS", "HCLTECH.NS", "KPIGREEN.NS", "DABUR.NS",
                 "KANSAINER.NS", "TATAPOWER.NS", "DEVYANI.NS", "^NSEI"]
tickerSymbols = ["BAJFINANCE"]

for i in tickerSymbols:
    analyze = Analyzer(i)
    analyze.readFile()
    analyze.getPercentageDetails()
    # analyze.writeToFile()
    # analyze.printdf()

outputDf.to_csv("companydetails.csv")
