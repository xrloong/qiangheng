#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector
from injector import inject

from optparse import OptionParser

from injection.module import PackageModule, ManagerModule, IOModule
from injection.module import CharacterModule

from model.StructureManager import StructureManager
from model.MainManager import MainManager

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
		mainManager.work()

def main():
	oparser = OptionParser()
	oparser.add_option("-p", dest = "package", help="package")
	oparser.add_option("-q", "--quiet", action = "store_true", dest="quiet", default=False)
	(options, args) = oparser.parse_args()

	qiangheng = QiangHeng(options)

if __name__ == "__main__":
	main()

