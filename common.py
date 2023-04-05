import re


def isInteger(value):
    return isinstance(value, str) and re.match("^(-)?\d+$", value) is not None
    

def isFloat(value):
    return isinstance(value, str) and re.match("^(-)?\d+\\.\d+$", value) is not None


def getColumnIndex(column):
    return ord(column) - ord("A")


def getColumnLetter(index):
    return chr(index + 65)
