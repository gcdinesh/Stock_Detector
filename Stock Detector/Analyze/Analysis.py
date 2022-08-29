import pandas as pd
from pandas import DataFrame
from os.path import exists
from datetime import datetime
from pandas_datareader import data

pd.set_option('display.max_columns', None)
file = pd.read_csv("../resources/StockTemplate.csv")
outputDf = DataFrame(file)

# if latest data needed replace 2022-08-23 with today's date


class Analyzer(object):
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        global outputDf
        self.resultDf = DataFrame()
        self.resultDf['Ticker Symbol'] = [self.tickerSymbol]
        self.resultDf['REJECT REASON'] = ""

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

    def getHighPriceWithinGivenDate(self, startDate, endDate):
        highPriceBeforeGivenDate = 0.0
        highPricedateBeforeGivenDate = "2007-06-01"

        for index, row in self.df.iterrows():
            # print(row['Date'] + " " + str(row['Close']))
            if(row['Date'] >= startDate and row['Date'] <= endDate):
                if(highPriceBeforeGivenDate < row['Close']):
                    highPriceBeforeGivenDate = row['Close']
                    highPricedateBeforeGivenDate = row['Date']
            elif(row['Date'] >= endDate):
                break

        # print(str(highPricedateBeforeGivenDate) +
        #       " " + str(highPriceBeforeGivenDate))
        self.highPriceWithinGivenDate = highPriceBeforeGivenDate
        self.highPriceDateWithinGivenDate = highPricedateBeforeGivenDate

    # Recovery time from 08 recession
    def getNumberOfYearsStockTookToRecoverFrom08Recession(self):
        self.resultDf['Recovery time from 08 recession'] = 0
        self.getHighPriceWithinGivenDate("2007-01-01", "2008-06-01")
        print(self.highPriceWithinGivenDate)
        print(self.highPriceDateWithinGivenDate)
        for index, row in self.df.iterrows():
            if(row['Date'] >= self.highPriceDateWithinGivenDate and
               row['Close'] > self.highPriceWithinGivenDate):
                print(row['Close'])
                print(row['Date'])
                date1 = datetime.strptime(row['Date'], "%Y-%m-%d")
                date2 = datetime.strptime(
                    self.highPriceDateWithinGivenDate, "%Y-%m-%d")
                noOfYears = (date1 - date2).days/365.0
                self.resultDf['Recovery time from 08 recession'] = noOfYears
                break

    # Is closing price before mar 20 is all time high?
    def isClosingPriceBeforeMar22IsAllTimeHigh(self):
        key = 'Is closing price before mar 22 is all time high?'
        self.getHighPriceWithinGivenDate("2000-01-01", "2020-03-08")
        date1 = datetime.strptime("2020-03-09", "%Y-%m-%d")
        date2 = datetime.strptime(self.df['Date'][0], "%Y-%m-%d")
        if(date2 <= date1):
            currentClosePrice = float(self.df.loc['2020-03-09']['Close'])
            if(self.highPriceWithinGivenDate != 0.0):
                diff = currentClosePrice - self.highPriceWithinGivenDate
                self.resultDf[key] = diff / \
                    (self.highPriceWithinGivenDate) * 100.0
                if(diff <= 0.0):
                    self.resultDf['REJECT REASON'] = self.resultDf['REJECT REASON'] + \
                        " Crossed high only because of covid"
        else:
            self.resultDf[key] = "recently listed"

    # Number of Years losses made
    # Number of Years Profit made
    # Max loss value for a year
    # Max Profit value for a year
    def numberOfYearsProfitAndLossMade(self):
        yearWiseReturns = self.getYearwiseStockIncrease(
            "2009-01-01", "2022-08-23")
        lossc = 0
        maxloss = 10000
        profitc = 0
        maxprofit = 0
        for i in yearWiseReturns:
            if(i <= 0.0):
                lossc = lossc + 1
                maxloss = min(maxloss, i)
            else:
                profitc = profitc + 1
                maxprofit = max(maxprofit, i)
        self.resultDf['Number of Years losses made'] = lossc
        self.resultDf['Number of Years Profit made'] = profitc
        self.resultDf['Max loss value for a year'] = maxloss
        self.resultDf['Max Profit value for a year'] = maxprofit
        if(lossc / (lossc + profitc) >= 0.6):
            self.resultDf['REJECT REASON'] = self.resultDf['REJECT REASON'] + \
                " Number of Loss years is greater than 59"

    # CAGR
    def cagr(self):
        key = 'CAGR'
        noOfYears = (datetime.strptime(
            self.df['Date'][-1], "%Y-%m-%d") -
            datetime.strptime(self.df['Date'][0], "%Y-%m-%d")).days/365
        CAGR = (self.df['Close'][-1]/self.df['Close'][0])**(1/noOfYears)-1
        self.resultDf[key] = CAGR * 100.0

    # CAGR after recession and before covid
    def cagrBeforeCovidAndAfterRecession(self):
        key = 'CAGR after recession and before covid'
        noOfYears = (datetime.strptime('2020-03-09', "%Y-%m-%d") -
                     datetime.strptime('2008-06-01', "%Y-%m-%d")).days/365
        self.getHighPriceWithinGivenDate("2008-05-01", "2008-08-01")
        recessionPeekValue = self.highPriceWithinGivenDate
        self.getHighPriceWithinGivenDate("2020-02-01", "2020-04-01")
        covidPeekValue = self.highPriceWithinGivenDate
        if(recessionPeekValue > 0.0):
            if(covidPeekValue > recessionPeekValue):
                CAGR = (covidPeekValue / recessionPeekValue)**(1/noOfYears)-1
                self.resultDf[key] = CAGR * 100.0
            else:
                self.resultDf["REJECT REASON"] = self.resultDf["REJECT REASON"] + \
                    " Was not able to grow beyond recession value"

    # Deviation from all time high

    def deviationFromAllTimeHigh(self):
        key = 'Deviation from all time high'
        self.getHighPriceWithinGivenDate("2000-01-01", "2022-08-23")
        currentClosePrice = float(self.df.loc['2022-08-23']['Close'])
        diff = currentClosePrice - self.highPriceWithinGivenDate
        if(diff > 0):
            self.resultDf[key] = diff / currentClosePrice
        else:
            self.resultDf[key] = diff / self.highPriceWithinGivenDate

    # REJECT REASON
    def rejectStockIfEvenAfterCovidStockDidNotTouchAllTimeHigh(self):
        key = 'REJECT REASON'
        self.getHighPriceWithinGivenDate("2000-01-01", "2020-03-01")
        highPriceBeforeCovid = self.highPriceWithinGivenDate
        self.getHighPriceWithinGivenDate("2020-03-02", "2022-08-23")
        highPriceAfterCovid = self.highPriceWithinGivenDate
        diff = highPriceAfterCovid - highPriceBeforeCovid
        if(diff <= 0.0):
            self.resultDf[key] = self.resultDf[key] + \
                " EVEN AFTER COVID NOT TOUCHED ALL TIME HIGH"

    # Number of years Growth between recession and covid?
    def numberOfYearsGrowthBetweenRecessionAndCovid(self):
        key = 'Number of years Growth between recession and covid'
        yearWiseReturns = self.getYearwiseStockIncrease(
            "2009-01-01", "2020-03-01")
        profitc = 0
        for i in yearWiseReturns:
            if(i > 0.0):
                profitc = profitc + 1
        self.resultDf[key] = profitc

    # Add latest price
    def latestPrice(self):
        key = 'Latest price'
        self.resultDf[key] = self.df['Close'][-1]

    # Recovery time for each year high to achieve more than 10% of invested value
    def getNumberOfYearsTakenFromThatYearHigh(self):
        noOfYears = 10
        year = 10
        average = 0.0
        for i in range(noOfYears):
            self.getHighPriceWithinGivenDate(
                "20" + str(year) + "-01-01", "20" + str(year + 1) + "-01-01")
            if(self.highPriceWithinGivenDate > 0.0):
                profitPrice = self.highPriceWithinGivenDate + self.highPriceWithinGivenDate * 0.1
                for index, row in self.df.iterrows():
                    if(row['Date'] >= self.highPriceDateWithinGivenDate and
                       row['Close'] > profitPrice):
                        date1 = datetime.strptime(row['Date'], "%Y-%m-%d")
                        date2 = datetime.strptime(
                            self.highPriceDateWithinGivenDate, "%Y-%m-%d")
                        noOfYears = (date1 - date2).days/365.0
                        average = average + noOfYears
                        self.resultDf["Recovery time for " + "20" + str(year) + "-"
                                      "20" + str(year + 1)] = noOfYears
                        break
            year = year + 1
        if(average > 0.0):
            self.resultDf["Average recovery time for each year high investment"] = average / 10

    def getYearwiseStockIncrease(self, startDate, endDate):
        yearWiseReturns = []
        prevPrice = 0.0
        prevDate = datetime.strptime(startDate, "%Y-%m-%d")
        finishDate = datetime.strptime(endDate, "%Y-%m-%d")
        for index, row in self.df.iterrows():
            currDate = datetime.strptime(row['Date'], "%Y-%m-%d")
            if(currDate >= prevDate and currDate < finishDate):
                if(prevPrice == 0.0):
                    prevPrice = row['Close']
                else:
                    currPrice = float(row['Close'])
                    diff = currPrice - prevPrice
                    if(diff > 0):
                        incrInPricePerYear = (diff/currPrice) * 100.0
                    else:
                        incrInPricePerYear = (diff/prevPrice) * 100.0
                    prevPrice = row['Close']
                    yearWiseReturns.append(incrInPricePerYear)
                prevDate = prevDate.replace(year=prevDate.year + 1)
        return yearWiseReturns

    def writeToFile(self):
        global outputDf
        outputDf = outputDf.append(self.resultDf, ignore_index=True)

    def printdf(self):
        print(outputDf)


# number of consecutive failures
# number of consecutive success
# add average of each year high investment
# replace \r\n with .NS", "
# tickerSymbols = ["INFY.NS", "HCLTECH.NS", "ICICIBANK.NS",
#                  "BANKBARODA.NS", "KOTAKBANK.NS", "SBIN.NS",
#                  "AXISBANK.NS", "HDFC.NS", "TECHM.NS", "ADANIGREEN.NS",
#                  "TATAPOWER.NS", "JSWENERGY.NS", "KPIGREEN.NS", "DEVYANI.NS",
#                  "JUBLFOOD.NS", "PVR.NS", "DABUR.NS", "COLPAL.NS"]

# NIFTY 50
tickerSymbols = ["ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
                 "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS",
                 "BHARTIARTL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS",
                 "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS",
                 "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS",
                 "HINDALCO.NS", "HINDUNILVR.NS", "HDFC.NS", "ICICIBANK.NS",
                 "ITC.NS", "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS",
                 "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS",
                 "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
                 "SBILIFE.NS", "SHREECEM.NS", "SBIN.NS", "SUNPHARMA.NS",
                 "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
                 "TECHM.NS", "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS"]

# NIFTY MIDCAP 150
# tickerSymbols = ["3MINDIA.NS", "ABB.NS", "AIAENG.NS", "APLAPOLLO.NS", "AUBANK.NS",
#                  "AAVAS.NS", "ABBOTINDIA.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS",
#                  "AFFLE.NS", "AJANTPHARM.NS", "APLLTD.NS", "ALKEM.NS", "ALKYLAMINE.NS",
#                  "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASTRAL.NS", "ATUL.NS", "AUROPHARMA.NS",
#                  "BALKRISIND.NS", "BANKINDIA.NS", "BATAINDIA.NS", "BAYERCROP.NS", "BEL.NS",
#                  "BHARATFORG.NS", "BHEL.NS", "BLUEDART.NS", "CGPOWER.NS", "CRISIL.NS",
#                  "CANBK.NS", "CLEAN.NS", "COFORGE.NS", "CONCOR.NS", "COROMANDEL.NS",
#                  "CROMPTON.NS", "CUMMINSIND.NS", "DALBHARAT.NS", "DEEPAKNTR.NS",
#                  "DELHIVERY.NS", "DIXON.NS", "LALPATHLAB.NS", "EMAMILTD.NS",
#                  "ENDURANCE.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS",
#                  "FORTIS.NS", "GMRINFRA.NS", "GICRE.NS", "GLAXO.NS", "GLENMARK.NS",
#                  "GODREJIND.NS", "GODREJPROP.NS", "GRINDWELL.NS", "FLUOROCHEM.NS",
#                  "GUJGASLTD.NS", "GSPL.NS", "HAPPSTMNDS.NS", "HATSUN.NS", "HAL.NS",
#                  "HINDPETRO.NS", "HINDZINC.NS", "HONAUT.NS", "ISEC.NS", "IDBI.NS",
#                  "IDFCFIRSTB.NS", "INDIAMART.NS", "INDIANB.NS", "IEX.NS", "INDHOTEL.NS",
#                  "IRCTC.NS", "IRFC.NS", "IGL.NS", "IPCALAB.NS", "JKCEMENT.NS",
#                  "JSWENERGY.NS", "JINDALSTEL.NS", "KAJARIACER.NS", "KANSAINER.NS",
#                  "L&TFH.NS", "LTTS.NS", "LICHSGFIN.NS", "LAURUSLABS.NS",
#                  "LINDEINDIA.NS", "MRF.NS", "LODHA.NS", "M&MFIN.NS",
#                  "MANAPPURAM.NS", "MFSL.NS", "MAXHEALTH.NS", "METROPOLIS.NS",
#                  "MPHASIS.NS", "NATCOPHARM.NS", "NHPC.NS", "NATIONALUM.NS",
#                  "NAVINFLUOR.NS", "NAM-INDIA.NS", "NUVOCO.NS", "OBEROIRLTY.NS",
#                  "OIL.NS", "OFSS.NS", "POLICYBZR.NS", "PAGEIND.NS",
#                  "PERSISTENT.NS", "PETRONET.NS", "PFIZER.NS", "PHOENIXLTD.NS",
#                  "POLYCAB.NS", "PFC.NS", "PRESTIGE.NS", "RECLTD.NS",
#                  "RAJESHEXPO.NS", "RELAXO.NS", "SKFINDIA.NS", "SANOFI.NS",
#                  "SCHAEFFLER.NS", "SRTRANSFIN.NS", "SOLARINDS.NS", "SONACOMS.NS",
#                  "STARHEALTH.NS", "SUMICHEM.NS", "SUNTV.NS", "SUNDARMFIN.NS",
#                  "SUNDRMFAST.NS", "SUPREMEIND.NS", "SYNGENE.NS", "TVSMOTOR.NS",
#                  "TATACHEM.NS", "TATACOMM.NS", "TATAELXSI.NS", "TTML.NS", "NIACL.NS",
#                  "RAMCOCEM.NS", "THERMAX.NS", "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TIINDIA.NS",
#                  "UNOMINDA.NS", "UNIONBANK.NS", "UBL.NS", "VBL.NS", "VINATIORGA.NS", "IDEA.NS",
#                  "VOLTAS.NS", "WHIRLPOOL.NS", "YESBANK.NS", "ZFCVINDIA.NS", "ZEEL.NS"]

# NIFTY SMALLCAP 100
# tickerSymbols = ["AEGISCHEM.NS", "ALLCARGO.NS", "ALOKINDS.NS", "AMARAJABAT.NS", "AMBER.NS",
#                  "ANGELONE.NS", "ANURAS.NS", "APTUS.NS", "AVANTIFEED.NS", "BASF.NS", "BSE.NS",
#                  "BAJAJELEC.NS", "BALAMINES.NS", "BALRAMCHIN.NS", "MAHABANK.NS", "BDL.NS",
#                  "BIRLACORPN.NS", "BSOFT.NS", "BRIGADE.NS", "BCG.NS", "MAPMYINDIA.NS",
#                  "CESC.NS", "CANFINHOME.NS", "CARBORUNIV.NS", "CENTRALBK.NS", "CDSL.NS",
#                  "CENTURYTEX.NS", "CHAMBLFERT.NS", "CHEMPLASTS.NS", "CUB.NS", "CAMS.NS",
#                  "CYIENT.NS", "DCMSHRIRAM.NS", "DELTACORP.NS", "DEVYANI.NS", "DBL.NS",
#                  "EIDPARRY.NS", "EDELWEISS.NS", "FINEORG.NS", "FSL.NS", "GMMPFAUDLR.NS",
#                  "GRANULES.NS", "GRAPHITE.NS", "GNFC.NS", "HEG.NS", "HFCL.NS", "HINDCOPPER.NS",
#                  "IDFC.NS", "IRB.NS", "IBULHSGFIN.NS", "IOB.NS", "INDIGOPNTS.NS",
#                  "INTELLECT.NS", "JBCHEPHARM.NS", "JKLAKSHMI.NS", "JMFINANCIL.NS",
#                  "JSL.NS", "JUBLINGREA.NS", "JUSTDIAL.NS", "KEI.NS", "KPITTECH.NS",
#                  "KALYANKJIL.NS", "KEC.NS", "LATENTVIEW.NS", "LXCHEM.NS", "LUXIND.NS",
#                  "MMTC.NS", "MGL.NS", "MASTEK.NS", "MEDPLUS.NS", "METROBRAND.NS",
#                  "MOTILALOFS.NS", "MCX.NS", "NBCC.NS", "PNBHOUSING.NS", "PVR.NS",
#                  "POONAWALLA.NS", "PRINCEPIPE.NS", "QUESS.NS", "RBLBANK.NS", "RADICO.NS",
#                  "RVNL.NS", "RAIN.NS", "REDINGTON.NS", "ROSSARI.NS", "ROUTE.NS", "SAPPHIRE.NS",
#                  "SOBHA.NS", "SONATSOFTW.NS", "STLTECH.NS", "SPARC.NS", "SUNTECK.NS",
#                  "SUZLON.NS", "TV18BRDCST.NS", "TANLA.NS", "UTIAMC.NS", "VIPIND.NS", "VTL.NS",
#                  "WELSPUNIND.NS", "ZENSARTECH.NS"]
tickerSymbols = ["BAJFINANCE.NS"]
# check SUNDARMFIN.NS average recovery time
for i in tickerSymbols:
    analyze = Analyzer(i)
    analyze.readFile()
    analyze.cleanse()
    analyze.latestPrice()
    analyze.cagrBeforeCovidAndAfterRecession()
    analyze.getNumberOfYearsStockTookToRecoverFrom08Recession()
    analyze.isClosingPriceBeforeMar22IsAllTimeHigh()
    analyze.deviationFromAllTimeHigh()
    analyze.numberOfYearsProfitAndLossMade()
    analyze.cagr()
    analyze.numberOfYearsGrowthBetweenRecessionAndCovid()
    analyze.getNumberOfYearsTakenFromThatYearHigh()
    analyze.rejectStockIfEvenAfterCovidStockDidNotTouchAllTimeHigh()
    analyze.writeToFile()
    print(outputDf)
outputDf.to_csv("output.csv")
