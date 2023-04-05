class Functions:
    def __init__(self):
        self._incr = -1
        pass

    def getGlobals(self):
        return {
            "concat": self._concat,
            "text": self._text,
            "incFrom": self._incFrom,
            "spread": self._spread,
            "split": self._split,
            "sum": self._sum,
            "bte": self._bte,
        }

    def _concat(self, *args):
        val = ""
        for str in args:
            val += str
        return val

    def _text(self, input):
        return str(input)
    
    def _incFrom(self, input):
        self._incr += 1
        return self._incr + input

    def _spread(self, args):
        return args
    
    def _split(self, input, separator):
        return input.split(separator)

    def _sum(self, args):
        sum = 0
        for num in args:
            sum += float(num)
        return sum
    
    def _bte(self, val1, val2):
        return float(val1) >= float(val2)
