class CodeMappingInfo:
    def __init__(self, name, code, variance):
        self.name = name
        self.code = code
        self.variance = variance

    def getKey(self):
        return [self.getCode(), self.getName(), self.getVariance()]

    def getName(self):
        return self.name

    def getCode(self):
        return self.code

    def getVariance(self):
        return self.variance
