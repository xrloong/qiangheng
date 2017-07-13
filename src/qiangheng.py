#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import Injector

from optparse import OptionParser
from model.MainManager import MainManager
from model import StateManager
from model.module import *

from Constant import MethodName, IsForIm, Quiet, OutputFormat

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

		def configure(binder):
			binder.bind(MethodName, to=methodName)
			binder.bind(IsForIm, to=isForIm)
			binder.bind(Quiet, to=quiet)
			binder.bind(OutputFormat, to=output_format)

		injector = Injector([configure, PackageModule()])

		imPackage = injector.get(Package)
		StateManager.setIMPackage(imPackage)
		mainManager=injector.get(MainManager)
		mainManager.write()

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

