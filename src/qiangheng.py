#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from optparse import OptionParser
from model import StateManager
from im.IMMgr import IMMgr
from model.StructureManager import StructureManager
from model.util.HanZiNetworkConverter import ComputeCharacterInfo

class QiangHeng:
	def __init__(self, options):
		inputMethod=options.input_method

		structureManager=StructureManager(inputMethod)
		computeCharacterInfo=ComputeCharacterInfo()
		characterInfoList=computeCharacterInfo.compute(structureManager)

		codeMappingInfoList=self.genIMMapping(characterInfoList)


		output_format=options.output_format
		isFormatXML=(output_format=='xml')
		isFormatYAML=(output_format=='yaml')
		isFormatTXT=(output_format=='text')
		isFormatQuiet=(output_format=='quiet')

		quiet=options.quiet or isFormatQuiet
		isToOutput=not quiet

		if isToOutput:
			if isFormatXML:
				from writer import XmlWriter
				writer = XmlWriter.XmlWriter()
			elif isFormatYAML:
				from writer import YamlWriter
				writer = YamlWriter.YamlWriter()
			elif isFormatTXT:
				from writer import TxtWriter
				writer = TxtWriter.TxtWriter()
			else:
				from writer import TxtWriter
				writer = TxtWriter.TxtWriter()
		else:
			# 不輸出結果
			from writer import QuietWriter
			writer = QuietWriter.QuietWriter()

		imInfo=structureManager.getImInfo()
		writer.write(imInfo, codeMappingInfoList)

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

def main():
	oparser = OptionParser()
	oparser.add_option("-i", "--im", "--input-method", dest="input_method", help="輸入法", default="cj")
	oparser.add_option("--format", type="choice", choices=["xml", "yaml", "text", "quiet"], dest="output_format", help="輸出格式，可能的選項有：xml、yaml、text、quiet", default="text")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet")
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

