#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector
from injector import inject

import ruamel.yaml

from optparse import OptionParser

from injection.module import PackageModule, ManagerModule, IOModule
from injection.module import CharacterModule
from injection.key import Writer
from injection.key import Characters

from coding.Base import CodingType
from coding.Base import CodeMappingInfoInterpreter
from model.StructureManager import StructureManager

from hanzi.network import HanZiNetwork
from hanzi.converter import ComputeCharacterInfo
from hanzi.helper import HanZiInterpreter

class QiangHeng:
	def __init__(self, options):
		packageName = options.package

		assert packageName, "需要使用 -p 來指定要載入的編碼法（輸入法或描繪法）模組名稱"

		package = __import__(packageName, fromlist=["coding"])

		quiet = options.quiet

		ioModule = IOModule(quiet)
		packageModule = PackageModule(package)
		injector = Injector([ioModule, packageModule])
		structureManager = injector.get(StructureManager)

		injector = Injector([ioModule, packageModule, ManagerModule(structureManager), CharacterModule()])
		mainManager = injector.get(MainManager)
		mainManager.compute()
		mainManager.write()


class MainManager:
	@inject
	def __init__(self,
			hanziNetwork: HanZiNetwork,
			structureManager: StructureManager,
			computeCharacterInfo: ComputeCharacterInfo,
			hanziInterpreter: HanZiInterpreter,
			codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
			writer: Writer,
			characters: Characters):
		self.hanziNetwork = hanziNetwork
		self.structureManager = structureManager
		self.computeCharacterInfo = computeCharacterInfo
		self.hanziInterpreter = hanziInterpreter
		self.codeMappingInfoInterpreter = codeMappingInfoInterpreter
		self.writer = writer

		self.characters = characters

	def compute(self):
		self.computeCharacterInfo.compute(self.characters)
		self.computeCharacterInfo.appendFastCodes()

	def write(self):
		characterInfoList = []
		for character in self.characters:
			charNode = self.hanziNetwork.findNode(character)
			if charNode:
				characterInfo = self.hanziInterpreter.interpretCharacterInfo(charNode)
				characterInfoList.append(characterInfo)
		characterInfoList = sorted(characterInfoList, key=lambda c: c.character)

		self.writer.write(characterInfoList, self.codeMappingInfoInterpreter)

def main():
	oparser = OptionParser()
	oparser.add_option("-p", dest = "package", help="package")
	oparser.add_option("-q", "--quiet", action = "store_true", dest="quiet", default=False)
	(options, args) = oparser.parse_args()

	qiangheng = QiangHeng(options)

if __name__ == "__main__":
	main()

