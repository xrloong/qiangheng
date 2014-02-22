#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from parser import ConfigParser
from optparse import OptionParser
from state import StateManager
from im.IMMgr import IMMgr
from description.CharacterDescriptionManager import CharacterDescriptionManager
from hanzi.HanZiNetwork import HanZiNetwork

class QiangHeng:
	def __init__(self, options):
		configFile=options.config_file

		output_format=options.output_format
		isFormatXML=(output_format=='xml')
		isFormatYAML=(output_format=='yaml')
		isFormatTXT=(output_format=='text')
		isFormatQuiet=(output_format=='quiet')

		quiet=options.quiet or isFormatQuiet
		isToOutput=not quiet

		configList=ConfigParser.ConfigParser().readConfig(configFile)
		[imProp, toTemplateList, toComponentList, toCodeList]=configList

		imPackage=IMMgr.getIMPackage(imProp)
		StateManager.setIMPackage(imPackage)

		StateManager.getCodeInfoManager().loadRadix(toCodeList)

		operationManager=StateManager.getOperationManager()
		self.descMgr=CharacterDescriptionManager(operationManager)
		self.descMgr.loadData(toTemplateList, toComponentList)

		self.hanziNetwork=HanZiNetwork.construct(self.descMgr)

		codeMappingInfoList=self.genIMMapping()
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

		imInfo=imPackage.IMInfo()
		writer.write(imInfo, codeMappingInfoList)

	def genIMMapping(self):
		characterFilter=lambda charName: (len(charName)==1)
#		targetCharacterList=[]
		targetCharacterList=filter(characterFilter, self.descMgr.getAllCharacters())
		table=[]
		for charName in sorted(targetCharacterList):
#			print("<-- %s -->"%charName, sys.stderr)
			characterInfo=self.hanziNetwork.getCharacterInfo(charName)
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

def main():
	oparser = OptionParser()
	oparser.add_option("-c", "--config", dest="config_file", help="輸入法設定檔", default="qhdata/config/default.xml")
	oparser.add_option("--format", type="choice", choices=["xml", "yaml", "text", "quiet"], dest="output_format", help="輸出格式，可能的選項有：xml、yaml、text、quiet", default="text")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet")
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

