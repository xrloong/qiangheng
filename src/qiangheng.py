#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector
from injector import inject

from optparse import OptionParser

from injection.module import PackageModule
from Constant import Package, CodingMethodName, IsForIm
from Constant import Quiet, OutputFormat
from Constant import Writer

from model.BaseCoding import CodingInfo
from model.element.CodingConfig import CodingConfig
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
			codingMethodName = inputMethod
			isForIm = True
		else:
			codingMethodName = drawMethod
			isForIm = False

		package = self.computeCodingPackage(codingMethodName)
		writer = self.computeWriter(isForIm, quiet, output_format)

		def configure(binder):
			binder.bind(CodingConfig, to=CodingConfig(package))
			binder.bind(CodingMethodName, to=codingMethodName)
			binder.bind(Package, to=package)
			binder.bind(Writer, to=writer)

		injector = Injector([configure, PackageModule()])

		mainManager=injector.get(MainManager)
		mainManager.compute()
		mainManager.write()

	def computeCodingPackage(self, codingMethodName):
		if codingMethodName in ['例', '範例', '範例輸入法', 'sample', 'sp',]:
			codingName='範例'
		elif codingMethodName in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
			codingName='倉頡'
		elif codingMethodName in ['行', '行列', '行列輸入法', 'array', 'ar',]:
			codingName='行列'
		elif codingMethodName in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
			codingName='大易'
		elif codingMethodName in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
			codingName='嘸蝦米'
		elif codingMethodName in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
			codingName='鄭碼'
		elif codingMethodName in ['四', '四角', '四角號碼', 'fourcorner', 'fc',]:
			codingName='四角'
		elif codingMethodName in ['庋', '庋㩪', '中國字庋㩪', 'guixie', 'gx',]:
			codingName='庋㩪'
		elif codingMethodName in ['動', '動組', '動態組字', 'dynamiccomposition', 'dc',]:
			codingName='動組'
		elif codingMethodName in ['筆順', 'strokeorder', 'so',]:
			codingName='筆順'
		else:
			assert False, "不知道的編碼法（輸入法、繪字法）: {method}".format(method=codingMethodName)
			codingName='不知道'

		if codingName == '範例':
			from im import Sample
			codingPackage=Sample
		elif codingName == '倉頡':
			from im import CangJie
			codingPackage=CangJie
		elif codingName == '行列':
			from im import Array
			codingPackage=Array
		elif codingName == '大易':
			from im import DaYi
			codingPackage=DaYi
		elif codingName == '嘸蝦米':
			from im import Boshiamy
			codingPackage=Boshiamy
		elif codingName == '鄭碼':
			from im import ZhengMa
			codingPackage=ZhengMa
		elif codingName == '四角':
			from im import FourCorner
			codingPackage=FourCorner
		elif codingName == '庋㩪':
			from im import GuiXie
			codingPackage=GuiXie
		elif codingName == '動組':
			from dm import DynamicComposition
			codingPackage=DynamicComposition
		elif codingName == '筆順':
			from dm import StrokeOrder
			codingPackage=StrokeOrder
		else:
			assert False, "不知道的編碼法（輸入法、繪字法）: {method}".format(method=codingMethodName)
			from model import DummyCoding
			codingPackage=DummyCoding

		return codingPackage

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

class MainManager:
	@inject
	def __init__(self, codingInfo: CodingInfo,
			computeCharacterInfo: ComputeCharacterInfo,
			writer: Writer):
		self.codingInfo = codingInfo
		self.computeCharacterInfo = computeCharacterInfo
		self.writer = writer

	def compute(self):
		self.characterInfoList = self.computeCharacterInfo.compute()

	def write(self):
		self.writer.write(self.codingInfo, self.characterInfoList)

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

