from pandas_datareader import data
from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd

tickers = ['ITC.NS']

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2000-01-01'
end_date = '2022-08-23'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader('ITC.NS', 'yahoo', start_date, end_date)


DataFrame(panel_data).to_csv("itc.csv")
