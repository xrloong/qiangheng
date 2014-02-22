import sys
import Constant
from xml.etree import ElementTree
from gear import OperatorManager
from parser import QHParser

class RadixManager:
	def __init__(self, codeInfoEncoder):
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}

		self.operationMgr=OperatorManager.OperatorManager(self)
		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	def setTurtleInfoList(self, charDescList):
		for charDesc in charDescList:
			charName=charDesc.getName()
			for structDesc in charDesc.getStructureList():
				if structDesc.isTurtle():
					codeVariance=structDesc.getCodeVarianceType()
					codeInfoProperties=structDesc.getCodeInfoDict()
					codeInfo=self.codeInfoEncoder.generateCodeInfo(codeInfoProperties)
					codeInfo.multiplyCodeVarianceType(codeVariance)

					radixCodeInfoList=self.radixCodeInfoDB.get(charName, [])
					radixCodeInfoList.append(codeInfo)
					self.radixCodeInfoDB[charName]=radixCodeInfoList
					pass
				else:
					print("型態錯誤", file=sys.stderr)

	def getRadixCodeInfo(self, radixName):
		return self.radixCodeInfoDB.get(radixName)[0]

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)


	def loadRadix(self, toRadixList):
		for filename in toRadixList:
			self.loadRadixFromXML(filename, fileencoding=Constant.FILE_ENCODING)

	def loadRadixFromXML(self, filename, fileencoding=Constant.FILE_ENCODING):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		radixInfoList=self.parser.loadCodeInfoByParsingXML(rootNode)
		self.setTurtleInfoList(radixInfoList)
#		self.radixList.extend(radixInfoList)

