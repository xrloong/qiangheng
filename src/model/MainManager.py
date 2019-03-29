from injector import inject

from Constant import Writer
from .base.IMInfo import IMInfo
from .util.HanZiNetworkConverter import ComputeCharacterInfo

class MainManager:
	@inject
	def __init__(self, imInfo: IMInfo,
			computeCharacterInfo: ComputeCharacterInfo,
			writer: Writer):
		self.imInfo = imInfo
		self.computeCharacterInfo = computeCharacterInfo
		self.writer = writer

	def compute(self):
		self.characterInfoList = self.computeCharacterInfo.compute()

	def write(self):
		self.writer.write(self.imInfo, self.characterInfoList)

