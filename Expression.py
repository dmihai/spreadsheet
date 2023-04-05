import re, copy

from common import getColumnIndex, isFloat, isInteger


class Expression:
    def __init__(self, expr, i, j, getCell, namedCols, functions):
        self._expr = expr
        self._i = i
        self._j = j
        self._getCell = getCell
        self._namedCols = namedCols
        self._functions = functions
    

    def parse(self):
        self._replaceNamedColumns()
        self._replaceLastValueFromGroup()
        self._replacePrevValueFromColumn()
        refs = self._getCellRefs()
        refValues = self._getCellValues(refs)

        if self._expr.find("^^") >= 0:
            self._expr = self._expr.replace("^^", "aboveValue")
            refValues.update({
                "aboveValue": self._getAboveValue(),
            })

        # print("----vars", refValues)

        try:
            value = eval(self._expr, self._functions.getGlobals(), refValues)
        except:
            value = "=" + self._expr
        
        # print("++++expr", self._expr, self._i, self._j, value)

        return value
    

    # get all references to individual cells from the expresion (e.g. D3, A6)
    def _getCellRefs(self):
        return re.findall("[A-Z]\d+", self._expr)
    

    # get values for a list of cells returning a dict (e.g. {D2:12, A6:Some_value})
    def _getCellValues(self, refs):
        values = {}
        for ref in refs:
            i = int(ref[1:]) - 1
            j = getColumnIndex(ref[0])

            values[ref] = self._getCell(i, j)["value"]

            if isInteger(values[ref]):
                values[ref] = int(values[ref])
            if isFloat(values[ref]):
                values[ref] = float(values[ref])
        
        return values
    

    # replace named columns like @adjusted_cost<1> with their corresponding cell (A8)
    def _replaceNamedColumns(self):
        cols = re.findall("@[A-Za-z_]+<\d+>", self._expr)
        for col in cols:
            parts = col[1:-1].split("<")
            namedCol = parts[0]
            colIndex = int(parts[1])
            if namedCol in self._namedCols:
                ref = self._namedCols[namedCol]
                self._expr = self._expr.replace(col, ref[0] + str(int(ref[1:]) + colIndex))

    
    # replace operands like E^v with their corresponding cell ref (e.g. E4)
    def _replaceLastValueFromGroup(self):
        refs = re.findall("[A-Z]\\^v", self._expr)
        for ref in refs:
            j = getColumnIndex(ref[0])
            for i in range(self._i-1, 0, -1):
                val = self._getCell(i, j)["value"]
                if val != "":
                    self._expr = self._expr.replace(ref, ref[0] + str(i+1))
                    break
    

    # replace operands like E^ with their corresponding cell ref (e.g. E3)
    # should be executed after _replaceLastGroupValue
    def _replacePrevValueFromColumn(self):
        refs = re.findall("[A-Z]\\^", self._expr)
        for ref in refs:
            self._expr = self._expr.replace(ref, ref[0] + str(self._i))
    

    # calculate the value for ^^
    def _getAboveValue(self):
        aboveField = self._getCell(self._i - 1, self._j)

        if aboveField["expr"] is not None:
            expr = copy.copy(aboveField["expr"])
            expr._replaceLastValueFromGroup()
            expr._replacePrevValueFromColumn()
            refs = expr._getCellRefs()
            for ref in refs:
                expr._expr = expr._expr.replace(ref, ref[0] + str(int(ref[1:]) + 1))
            return expr.parse()
        else:
            return aboveField["value"]
