import csv

from Spreadsheet import Spreadsheet


def exportToCsv(file, data):
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

data = Spreadsheet()
data.loadFromCsv('transactions.csv')
data.computeValues()
values = data.getValues()
exportToCsv('output.csv', values)
