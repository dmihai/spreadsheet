import csv

from Expression import Expression
from Functions import Functions
from common import getColumnLetter, isFloat, isInteger

class Spreadsheet:
    def __init__(self):
        self._data = []
        self._functions = Functions()
        self._namedCols = {}
    
    def loadFromCsv(self, file):
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            self._data = []
            for row in reader:
                line = []
                for field in row:
                    line.append({
                        "input": field,
                        "value": "",
                        "expr": None,
                    })
                self._data.append(line)
    

    def computeValues(self):
        for i in range(len(self._data)):
            for j in range(len(self._data[i])):
                self._data[i][j] = self._computeValue(i, j)
                if self._data[i][j]["expr"]:
                    self._data[i][j]["value"] = self._data[i][j]["expr"].parse()
                
                if isInteger(self._data[i][j]["value"]):
                    self._data[i][j]["value"] = int(self._data[i][j]["value"])
                if isFloat(self._data[i][j]["value"]):
                    self._data[i][j]["value"] = float(self._data[i][j]["value"])
    

    def getValues(self):
        values = []
        for row in self._data:
            line = []
            for cell in row:
                line.append(cell["value"])
            values.append(line)
        return values


    def _computeValue(self, i, j):
        field = self._data[i][j].copy()
        input = field["input"]

        if input.startswith("!"):
            field["value"] = input[1:]
            self._namedCols[field["value"]] = getColumnLetter(j) + str(i+1)
        elif input.startswith("="):
            field["expr"] = Expression(input[1:], i, j, self._computeValue, self._namedCols, self._functions)
        else:
            field["value"] = input
        
        return field
