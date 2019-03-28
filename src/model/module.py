from injector import Module
from injector import provider, singleton

from . import StateManager
from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import CharacterDescriptionManager
from model.hanzi import HanZiNetwork
import model.base

from Constant import MethodName, Package, IsForIm, Quiet, OutputFormat, Writer
from Constant import MainCharDescManager, ImCharDescManager

class PackageModule(Module):
	@provider
	def providePackage(self, isForIm: IsForIm, methodName: MethodName) -> Package:
		if isForIm:
			return getImPackage(methodName)
		else:
			return getDmPackage(methodName)

	@provider
	def provideIMInfo(self, package: Package) -> model.base.IMInfo:
		return package.IMInfo()

	@provider
	def provideOperatorManager(self) -> model.OperatorManager.OperatorManager:
		return StateManager.getOperationManager()

	@provider
	def provideCodeInfoManager(self) -> model.CodeInfoManager.CodeInfoManager:
		return StateManager.getCodeInfoManager()

	@singleton
	@provider
	def provideStructureManager(self, inputMethod: MethodName, \
			operationManager: model.OperatorManager.OperatorManager, \
			codeInfoManager: model.CodeInfoManager.CodeInfoManager, \
			mainCharDescManager: MainCharDescManager, \
			imCharDescManager: ImCharDescManager \
			) -> StructureManager:
		return StructureManager(inputMethod, operationManager, codeInfoManager,
				mainCharDescManager, imCharDescManager)

	@singleton
	@provider
	def provideMainCharDescManager(self, charDescManager: CharacterDescriptionManager) -> MainCharDescManager:
		return charDescManager

	@singleton
	@provider
	def provideImCharDescManager(self, charDescManager: CharacterDescriptionManager) -> ImCharDescManager:
		return charDescManager

	@singleton
	@provider
	def provideHanZiNetwork(self) -> HanZiNetwork:
		return HanZiNetwork()

	@provider
	def provideWriter(self, isForIm: IsForIm, quiet: Quiet, outputFormat: OutputFormat) -> Writer:
		self.isForIm = isForIm
		return self.getWriter(quiet, outputFormat)

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

