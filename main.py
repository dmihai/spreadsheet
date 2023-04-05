from Spreadsheet import Spreadsheet


data = Spreadsheet()
data.loadFromCsv('transactions.csv')
data.computeValues()
print(data.getValues())
