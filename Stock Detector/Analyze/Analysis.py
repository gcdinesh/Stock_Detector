import pandas as pd
import yfinance as yf
from pandas import DataFrame
from os.path import exists
from datetime import datetime
from datetime import timedelta
from datetime import date

pd.set_option('display.max_columns', None)
file = pd.read_csv("../resources/StockTemplate.csv")
outputDf = DataFrame(file)


class Analyzer(object):
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        global outputDf
        self.resultDf = DataFrame()
        self.resultDf['Ticker Symbol'] = [self.tickerSymbol]

    def readFile(self):
        filePath = "C:/Users/gcdin/Downloads/" + self.tickerSymbol + ".csv"
        fileExists = exists(filePath)
        if(not fileExists):
            print("File does not exist. Fetching it for: " + self.tickerSymbol)
            finData = yf.Ticker(self.tickerSymbol)
            hist = finData.history(period="max")
            hist.to_csv(filePath)
        else:
            print("File Exists for: " + self.tickerSymbol)
        file = pd.read_csv(filePath)
        self.df = DataFrame(file)

    def cleanse(self):
        self.df = self.df.drop(['Open', 'High', 'Low', 'Volume'], axis=1)
        self.df = self.df.dropna()
        self.df.index = self.df['Date']

    def getHighPriceDateBeforeGivenDate(self, endDate):
        highPriceBeforeGivenDate = 0.0
        highPricedateBeforeGivenDate = "2007-06-01"

        for index, row in self.df.iterrows():
            # print(row['Date'] + " " + str(row['Close']))
            if(row['Date'] >= "2007-06-01" and row['Date'] <= endDate):
                if(highPriceBeforeGivenDate < row['Close']):
                    highPriceBeforeGivenDate = row['Close']
                    highPricedateBeforeGivenDate = row['Date']
            elif(row['Date'] >= endDate):
                break

        # print(str(highPricedateBeforeGivenDate) +
        #       " " + str(highPriceBeforeGivenDate))
        self.highPriceBeforeGivenDate = highPriceBeforeGivenDate
        self.highPricedateBeforeGivenDate = highPricedateBeforeGivenDate

    # Recovery time from 08 recession
    def getNumberOfYearsStockTookToRecoverFrom08Recession(self):
        self.resultDf['Recovery time from 08 recession'] = 0
        self.getHighPriceDateBeforeGivenDate("2008-06-01")
        for index, row in self.df.iterrows():
            if(row['Date'] >= self.highPricedateBeforeGivenDate and
               row['Close'] > self.highPriceBeforeGivenDate):
                date1 = datetime.strptime(row['Date'], "%Y-%m-%d")
                date2 = datetime.strptime(
                    self.highPricedateBeforeGivenDate, "%Y-%m-%d")
                noOfYears = (date1 - date2).days/365.0
                self.resultDf['Recovery time from 08 recession'] = noOfYears
                break

    # Does closing price before mar 22 is all time high?
    def doesClosingPriceBeforeMar22IsAllTimeHigh(self):
        key = 'Does closing price before mar 22 is all time high?'
        self.getHighPriceDateBeforeGivenDate("2020-03-10")
        currentClosePrice = float(self.df.loc['2022-08-01']['Close'])
        self.resultDf[key] = (
            currentClosePrice - self.highPriceBeforeGivenDate) / (self.highPriceBeforeGivenDate) * 100.0

    # Stock raised only because of covid?
    def stockRaisedOnlyBecauseOfCovid(self):
        key = 'Stock raised only because of covid?'
        self.resultDf[key] = True
        prevPrice = 0.0
        prevDate = datetime.strptime("2009-01-01", "%Y-%m-%d")
        for index, row in self.df.iterrows():
            currDate = datetime.strptime(row['Date'], "%Y-%m-%d")
            if(currDate >= prevDate):
                if(prevPrice == 0.0):
                    prevPrice = row['Close']
                else:
                    currPrice = float(row['Close'])
                    print(currDate)
                    incrInPricePerYear = (
                        (currPrice - prevPrice)/currPrice) * 100.0
                    print(str(incrInPricePerYear))
                    print("******************")
                    prevPrice = row['Close']
                prevDate = prevDate.replace(year=prevDate.year + 1)

    def writeToFile(self):
        global outputDf
        outputDf = outputDf.append(self.resultDf, ignore_index=True)

    def printdf(self):
        print(outputDf)


tickerSymbols = ["GOLDTECH.NS", "ITC.NS"]
for i in tickerSymbols:
    analyze = Analyzer(i)
    analyze.readFile()
    analyze.cleanse()
    analyze.getNumberOfYearsStockTookToRecoverFrom08Recession()
    analyze.doesClosingPriceBeforeMar22IsAllTimeHigh()
    analyze.stockRaisedOnlyBecauseOfCovid()
    analyze.writeToFile()
    print(outputDf)
outputDf.to_csv("output.csv")
