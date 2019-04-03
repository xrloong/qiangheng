from injector import inject
from injector import singleton

from Constant import Package

from parser.QHParser import QHRadixParser
from model.BaseCoding import CodeInfoEncoder

@singleton
class CodeInfoManager:
	@inject
	def __init__(self, radixParser: QHRadixParser):
		self.radixParser=radixParser
		self.radixCodeInfoDB={}
		self.resetRadixList=[]

	def loadRadix(self, radixFileList):
		[self.resetRadixList, self.radixCodeInfoDB]=self.radixParser.loadRadix(radixFileList)

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)

	def hasResetRadix(self, radixName):
		return (radixName in self.resetRadixList)

	def getResetRadixList(self):
		return self.resetRadixList


