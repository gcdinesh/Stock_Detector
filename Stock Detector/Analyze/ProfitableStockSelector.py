import pandas as pd
from pandas import DataFrame
from os.path import exists
from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yfin

pd.set_option('display.max_columns', None)
yfin.pdr_override()


# if latest data needed replace 2022-08-23 with today's date


class ProfitableStockSelector(object):
    def __init__(self, tickerSymbol):
        self.tickerSymbol = tickerSymbol
        global outputDf
        self.resultDf = DataFrame()
        self.resultDf['Ticker Symbol'] = [self.tickerSymbol]

    def readFile(self):
        filePath = "C:/Users/gcdin/Downloads/yahoo/" + self.tickerSymbol + ".csv"
        fileExists = exists(filePath)
        if(not fileExists):
            # print("File does not exist. Fetching it for: " + self.tickerSymbol)
            panel_data = pdr.get_data_yahoo(
                self.tickerSymbol, start='2020-01-01', end='2023-02-02')
            DataFrame(panel_data).to_csv(filePath)
        # else:
            # print("File Exists for: " + self.tickerSymbol)
        file = pd.read_csv(filePath)
        self.df = DataFrame(file)

    def cleanse(self):
        self.df = self.df.drop(['Open', 'High', 'Low', 'Volume'], axis=1)
        self.df = self.df.dropna()
        self.df.index = self.df['Date']

    # startdate should be today's date
    def getHighPriceWithinGivenDate(self):
        startDate = "2022-02-02"
        endDate = "2023-02-01"
        i = 10
        prev = 0
        count = 0
        for index, row in self.df.iterrows():
            print(row['Date'] + " " + str(row['Close']))
            if(row['Date'] >= startDate and row['Date'] <= endDate and i == 10):
                i = 0
                print(row['Date'] + " " + str(row['Close']))
                if(row['Close'] >= prev):
                    count = count + 1
                    prev = row['Close']
            i = i + 1

        print(str(count) + " " + str(self.tickerSymbol))
        if(count > 0 and count/26 > 0.0):
            print(str(count/26) + " " + str(self.tickerSymbol))


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
tickerSymbols = ["INFY.NS"]

for i in tickerSymbols:
    analyze = ProfitableStockSelector(i)
    analyze.readFile()
    analyze.cleanse()
    analyze.getHighPriceWithinGivenDate()
