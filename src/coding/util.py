import yaml

def readCodingInfo(infoFile):
    return YamlFileCodingInfo(infoFile)

class YamlFileCodingInfo:
    def __init__(self, infoFile):
        self.infoFile = infoFile
        self.root = yaml.load(open(infoFile), yaml.SafeLoader)
        self.codingInfo = self.root['編碼法資訊']

    def getName(self, region):
        return self.codingInfo['顯示名稱'].get(region)

    def getKeyMaps(self):
        return self.codingInfo['按鍵對應']

    def getMaxKeyLength(self):
        return self.codingInfo['最大長度']

