#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector
from injector import inject

from optparse import OptionParser

from injection.module import PackageModule, ManagerModule
from Constant import Package
from Constant import Quiet, OutputFormat
from Constant import Writer

from coding.Base import CodingInfo
from coding.Base import CodingType
from model.element.CodingConfig import CodingConfig
from model.StructureManager import StructureManager

from hanzi.network import HanZiNetwork
from hanzi.converter import ComputeCharacterInfo
from hanzi.helper import HanZiInterpreter

class QiangHeng:
	def __init__(self, options):
		packageName=options.package

		assert packageName, "需要使用 -p 來指定要載入的編碼法（輸入法或描繪法）模組名稱"

		package = __import__(packageName, fromlist=["coding"])

		quiet=options.quiet


		writer = self.computeWriter(package.codingType, quiet)

		def configure(binder):
			binder.bind(CodingConfig, to=CodingConfig(package))
			binder.bind(Package, to=package)
			binder.bind(Writer, to=writer)

		injector = Injector([configure, PackageModule()])
		structureManager = injector.get(StructureManager)

		injector = Injector([configure, PackageModule(), ManagerModule(structureManager)])
		mainManager=injector.get(MainManager)
		mainManager.compute()
		mainManager.write()


	def computeWriter(self, codingType, quiet: Quiet) -> Writer:
		self.isForIm = (CodingType.Input == codingType)
		return self.getWriter(quiet)

	def getWriter(self, quiet=False):
		isToOutput = not quiet
		if isToOutput:
			writer = self.getYamlWriter()
		else:
			# 不輸出結果
			writer = self.getQuietWriter()
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
			hanziNetwork: HanZiNetwork,
			structureManager: StructureManager,
			computeCharacterInfo: ComputeCharacterInfo,
			hanziInterpreter: HanZiInterpreter,
			writer: Writer):
		self.codingInfo = codingInfo
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.computeCharacterInfo = computeCharacterInfo
		self.hanziInterpreter = hanziInterpreter
		self.writer = writer

		self.characters = self.generateTargetCharacters()

	def generateTargetCharacters(self):
#		characters = self.structureManager.getAllCharacters()

		import itertools
		rangeCJK = range(0x4e00, 0x9fa5+1)
		rangeCJKextA = range(0x3400, 0x4db5+1)
		characters = [chr(c) for c in itertools.chain(rangeCJK, rangeCJKextA)]
		return characters

	def compute(self):
		self.computeCharacterInfo.compute(self.characters)

	def write(self):
		characterInfoList = []
		for character in self.characters:
			charNode = self.hanziNetwork.findNode(character)
			if charNode:
				characterInfo = self.hanziInterpreter.interpretCharacterInfo(charNode)
				characterInfoList.append(characterInfo)
		characterInfoList = sorted(characterInfoList, key=lambda c: c.character)

		self.writer.write(self.codingInfo, characterInfoList)

def main():
	oparser = OptionParser()
	oparser.add_option("-p", dest="package", help="package")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False)
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

