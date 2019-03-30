#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector
from injector import inject

from optparse import OptionParser

from injection.module import PackageModule
from Constant import Package, MethodName, IsForIm
from Constant import Quiet, OutputFormat
from Constant import Writer

from model.base.IMInfo import IMInfo
from model.base.CodingConfig import CodingConfig
from model.util.HanZiNetworkConverter import ComputeCharacterInfo

class QiangHeng:
	def __init__(self, options):
		inputMethod=options.input_method
		drawMethod=options.draw_method

		assert inputMethod or drawMethod, "需要使用 -i 來指定輸入法或使用 -d 來使用描繪法"
		assert (not inputMethod or not drawMethod), "不能同時使用 -i 來指定輸入法和用 -d 來使用描繪法"

		output_format=options.output_format
		quiet=options.quiet

		if inputMethod:
			methodName = inputMethod
			isForIm = True
		else:
			methodName = drawMethod
			isForIm = False

		package = self.computePackage(isForIm, methodName)
		writer = self.computeWriter(isForIm, quiet, output_format)

		def configure(binder):
			binder.bind(CodingConfig, to=self.getCodingConfig(methodName))
			binder.bind(MethodName, to=methodName)
			binder.bind(Package, to=package)
			binder.bind(Writer, to=writer)

		injector = Injector([configure, PackageModule()])

		mainManager=injector.get(MainManager)
		mainManager.compute()
		mainManager.write()

	def computePackage(self, isForIm, methodName):
		if isForIm:
			return self.getImPackage(methodName)
		else:
			return self.getDmPackage(methodName)

	def getImPackage(self, imName):
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
			from model.im import CangJie
			imPackage=CangJie
		elif imName == '行列':
			from model.im import Array
			imPackage=Array
		elif imName == '大易':
			from model.im import DaYi
			imPackage=DaYi
		elif imName == '嘸蝦米':
			from model.im import Boshiamy
			imPackage=Boshiamy
		elif imName == '鄭碼':
			from model.im import ZhengMa
			imPackage=ZhengMa
		elif imName == '四角':
			from model.im import FourCorner
			imPackage=FourCorner
		elif imName == '庋㩪':
			from model.im import GuiXie
			imPackage=GuiXie
		elif imName == '範例':
			from model.im import Sample
			imPackage=Sample
		else:
			assert False, "不知道的輸入法: %s"%imName

		return imPackage

	def getDmPackage(self, dmName):
		if dmName in ['動', '動組', '動態組字', 'dynamiccomposition', 'dc',]:
			dmName='動組'
		elif dmName in ['筆順', 'strokeorder', 'so',]:
			dmName='筆順'
		else:
			assert False, "不知道的繪字法: %s"%dmName
			dmName='不知道'

		if dmName == '動組':
			from model.dm import DynamicComposition
			dmPackage=DynamicComposition
		elif dmName == '筆順':
			from model.dm import StrokeOrder
			dmPackage=StrokeOrder
		else:
			assert False, "不知道的繪字法: %s"%dmName

		return dmPackage

	def computeWriter(self, isForIm: IsForIm, quiet: Quiet, outputFormat: OutputFormat) -> Writer:
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
			from writer.im import TxtWriter
		else:
			from writer.dm import TxtWriter
		writer = TxtWriter()
		return writer

	def getXmlWriter(self):
		if self.isForIm:
			from writer.im import XmlWriter
		else:
			from writer.dm import XmlWriter
		writer = XmlWriter()
		return writer

	def getYamlWriter(self):
		if self.isForIm:
			from writer.im import YamlWriter
		else:
			from writer.dm import YamlWriter
		writer = YamlWriter()
		return writer

	def getQuietWriter(self):
		if self.isForIm:
			from writer.im import QuietWriter
		else:
			from writer.dm import QuietWriter
		writer = QuietWriter()
		return writer

	def getCodingConfig(self, codingMethodName):
		return CodingConfig(
			self.getMainComponentList(),
			self.getMainTemplateFile(),
			self.getIMComponentList(codingMethodName),
			self.getIMSubstituteFile(codingMethodName),
			self.getIMRadixList(codingMethodName),
			)
        
	def getMainComponentList(self):
		mainDir = self.getMainDir()
		mainComponentList = [
			mainDir + 'CJK.yaml',
			mainDir + 'CJK-A.yaml',
			mainDir + 'component/CJK.yaml',
			mainDir + 'component/CJK-A.yaml',
			mainDir + 'style.yaml',
		]
		return mainComponentList

	def getMainTemplateFile(self):
		mainDir = self.getMainDir()
		mainTemplateFile = mainDir + 'template.yaml'
		return mainTemplateFile

	def getIMComponentList(self, methodName: MethodName):
		methodDir = self.getMethodDir(methodName)
		methodComponentList = [
			methodDir + 'style.yaml',
		]
		return methodComponentList

	def getIMSubstituteFile(self, methodName: MethodName):
		methodDir = self.getMethodDir(methodName)
		meethodSubstituteFile = methodDir + 'substitute.yaml'
		return meethodSubstituteFile

	def getIMRadixList(self, methodName: MethodName):
		methodDir = self.getMethodDir(methodName)
		methodRadixList = [
			methodDir + 'radix/CJK.yaml',
			methodDir + 'radix/CJK-A.yaml',
			methodDir + 'radix/adjust.yaml'
		]
		return methodRadixList

	def getMainDir(self):
		return "gen/qhdata/main/"

	def getMethodDir(self, methodName):
		return "gen/qhdata/{method}/".format(method=methodName)

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

def main():
	oparser = OptionParser()
	oparser.add_option("-i", "--im", "--input-method", dest="input_method", help="輸入法")
	oparser.add_option("-d", "--dm", "--draw-method", dest="draw_method", help="描繪法")
	oparser.add_option("--format", type="choice", choices=["xml", "yaml", "text", "quiet"], dest="output_format", help="輸出格式，可能的選項有：xml、yaml、text、quiet", default="text")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False)
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

