import argparse
import csv

from Spreadsheet import Spreadsheet


def exportToCsv(file, data):
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

inputFile = 'transactions.csv'
outputFile = 'output.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=False, default=inputFile,
                    help='Input csv file name')
parser.add_argument('--output', type=str, required=False, default=outputFile,
                    help='Output csv file name')
args = parser.parse_args()

data = Spreadsheet()
data.loadFromCsv(args.input)
data.computeValues()
values = data.getValues()
exportToCsv(args.output, values)
