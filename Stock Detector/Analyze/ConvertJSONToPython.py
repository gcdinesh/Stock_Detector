import json
import csv
from os.path import exists
import requests


# print(x.text)


class MutualFundUtil(object):
    def __init__(self, path, tickerSymbol):
        self.path = path
        self.tickerSymbol = tickerSymbol

    def generateFile(self):
        filePath = "C:/Users/gcdin/Downloads/yahoo/" + self.tickerSymbol + ".json"
        fileExists = exists(filePath)
        if(not fileExists):
            print("File does not exist. Fetching it for: " + self.tickerSymbol)
            x = requests.get(self.path)
            with open(filePath, 'w') as f:
                f.write(x.text)

        else:
            print("File Exists for: " + self.tickerSymbol)

        with open(filePath) as json_file:
            data = json.load(json_file)
        employee_data = data['data']

        # now we will open a file for writing
        csvfilePath = "C:/Users/gcdin/Downloads/yahoo/" + self.tickerSymbol + ".csv"
        data_file = open(csvfilePath, 'w', newline='', encoding='utf-8')

        # create the csv writer object
        csv_writer = csv.writer(data_file)
        header = ['Date', 'Close']
        csv_writer.writerow(header)
        for emp in employee_data:
            csv_writer.writerow(emp.values())

        data_file.close()
