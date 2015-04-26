from . import StateManager
from .StructureManager import StructureManager
from .util.HanZiNetworkConverter import ComputeCharacterInfo

class MainManager:
	def __init__(self, methodName, methodPackage):
		StateManager.setIMPackage(methodPackage)
		self.imInfo=methodPackage.IMInfo()

		self.structureManager=StructureManager(methodName)
		computeCharacterInfo=ComputeCharacterInfo()
		self.characterInfoList=computeCharacterInfo.compute(self.structureManager)

	@staticmethod
	def generateInputMethod(inputMethodName):
		imPackage=getImPackage(inputMethodName)
		mainManager=MainManager(inputMethodName, imPackage)
		mainManager.isForIm=True
		return mainManager

	@staticmethod
	def generateDrawMethod(drawMethodName):
		dmPackage=getDmPackage(drawMethodName)
		mainManager=MainManager(drawMethodName, dmPackage)
		mainManager.isForIm=False
		return mainManager

	def write(self, quiet, output_format):
		codeMappingInfoList=self.genIMMapping(self.characterInfoList)
		imInfo=self.imInfo

		writer=self.getWriter(quiet, output_format)
		writer.write(imInfo, codeMappingInfoList)

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

	def getWriter(self, quiet=False, output_format="text"):
		isFormatXML=(output_format=='xml')
		isFormatYAML=(output_format=='yaml')
		isFormatTXT=(output_format=='text')
		isFormatQuiet=(output_format=='quiet')

		isToOutput=not quiet and not isFormatQuiet
		if isToOutput:
			if isFormatXML:
				writer = self.getXmlWriter()
			elif isFormatYAML:
				writer = self.getYamlWriter()
			elif isFormatTXT:
				writer = self.getTextWriter()
			else:
				writer = self.getTextWriter()
		else:
			# 不輸出結果
			writer = self.getQuietWriter()
		return writer

	def getTextWriter(self):
		if self.isForIm:
			from .im.writer import TxtWriter
		else:
			from .dm.writer import TxtWriter
		writer = TxtWriter.TxtWriter()
		return writer

	def getXmlWriter(self):
		if self.isForIm:
			from .im.writer import XmlWriter
		else:
			from .dm.writer import XmlWriter
		writer = XmlWriter.XmlWriter()
		return writer

	def getYamlWriter(self):
		if self.isForIm:
			from .im.writer import YamlWriter
		else:
			from .dm.writer import YamlWriter
		writer = YamlWriter.YamlWriter()
		return writer

	def getQuietWriter(self):
		if self.isForIm:
			from .im.writer import QuietWriter
		else:
			from .dm.writer import QuietWriter
		writer = QuietWriter.QuietWriter()
		return writer

def getImPackage(imName):
	if imName in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
		imName='倉頡'
	elif imName in ['行', '行列', '行列輸入法', 'array', 'ar',]:
		imName='行列'
	elif imName in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
		imName='大易'
	elif imName in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
		imName='嘸蝦米'
	elif imName in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
		imName='鄭碼'
	elif imName in ['四', '四角', '四角號碼', 'fourcorner', 'fc',]:
		imName='四角'
	elif imName in ['庋', '庋㩪', '中國字庋㩪', 'guixie', 'gx',]:
		imName='庋㩪'
	elif imName in ['例', '範例', '範例輸入法', 'sample', 'sample',]:
		imName='範例'
	else:
		assert False, "不知道的輸入法: %s"%imName
		imName='不知道'

	if imName == '倉頡':
		from .im import CangJie
		imPackage=CangJie
	elif imName == '行列':
		from .im import Array
		imPackage=Array
	elif imName == '大易':
		from .im import DaYi
		imPackage=DaYi
	elif imName == '嘸蝦米':
		from .im import Boshiamy
		imPackage=Boshiamy
	elif imName == '鄭碼':
		from .im import ZhengMa
		imPackage=ZhengMa
	elif imName == '四角':
		from .im import FourCorner
		imPackage=FourCorner
	elif imName == '庋㩪':
		from .im import GuiXie
		imPackage=GuiXie
	elif imName == '範例':
		from .im import Sample
		imPackage=Sample
	else:
		assert False, "不知道的輸入法: %s"%imName

	return imPackage

def getDmPackage(dmName):
	if dmName in ['動', '動組', '動態組字', 'dynamiccomposition', 'dc',]:
		dmName='動組'
	elif dmName in ['筆順', 'strokeorder', 'so',]:
		dmName='筆順'
	else:
		assert False, "不知道的繪字法: %s"%dmName
		dmName='不知道'

	if dmName == '動組':
		from .dm import DynamicComposition
		dmPackage=DynamicComposition
	elif dmName == '筆順':
		from .dm import StrokeOrder
		dmPackage=StrokeOrder
	else:
		assert False, "不知道的繪字法: %s"%dmName

	return dmPackage

