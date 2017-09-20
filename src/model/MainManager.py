from injector import inject

from Constant import IsForIm, Quiet, OutputFormat, Writer
from .base.IMInfo import IMInfo
from .util.HanZiNetworkConverter import ComputeCharacterInfo

class MainManager:
	@inject
	def __init__(self, \
			imInfo: IMInfo, isForIm: IsForIm, \
			quiet: Quiet, outputFormat: OutputFormat, \
			computeCharacterInfo: ComputeCharacterInfo, \
			writer: Writer):
		self.isForIm = isForIm
		self.imInfo = imInfo
		self.quiet = quiet
		self.outputFormat = outputFormat
		self.characterInfoList = computeCharacterInfo.compute()
		self.writer = writer

	def write(self):
		self.writer.write(self.imInfo, self.characterInfoList)

