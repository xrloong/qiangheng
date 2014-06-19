#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from optparse import OptionParser
from state import StateManager
from im.IMMgr import IMMgr
from description.CharacterDescriptionManager import CharacterDescriptionManager
from hanzi.HanZiNetwork import HanZiNetwork

class QiangHeng:
	def __init__(self, options):
		inputMethod=options.input_method
		toTemplateList = [
			'gen/qhdata/main/template.yaml',
		]
		toComponentList = [
			'gen/qhdata/main/CJK.yaml',
			'gen/qhdata/main/CJK-A.yaml',
			'gen/qhdata/main/component/CJK.yaml',
			'gen/qhdata/main/component/CJK-A.yaml',
			'gen/qhdata/main/style.yaml',
			'gen/qhdata/%s/style.yaml'%inputMethod,
			'gen/qhdata/%s/component/CJK.yaml'%inputMethod,
			'gen/qhdata/%s/component/CJK-A.yaml'%inputMethod,
		]
		toCodeList = [
			'gen/qhdata/%s/radix/CJK.yaml'%inputMethod,
			'gen/qhdata/%s/radix/CJK-A.yaml'%inputMethod,
		]
		toSutstitueFile = 'gen/qhdata/%s/substitute.yaml'%inputMethod

		imPackage=IMMgr.getIMPackage(inputMethod)

		output_format=options.output_format
		isFormatXML=(output_format=='xml')
		isFormatYAML=(output_format=='yaml')
		isFormatTXT=(output_format=='text')
		isFormatQuiet=(output_format=='quiet')

		quiet=options.quiet or isFormatQuiet
		isToOutput=not quiet

		StateManager.setIMPackage(imPackage)

		StateManager.getCodeInfoManager().loadRadix(toCodeList)
		StateManager.getOperationManager().loadSubstituteRules(toSutstitueFile)

		self.descMgr=CharacterDescriptionManager()
		self.descMgr.loadData(toTemplateList, toComponentList)

		self.hanziNetwork=HanZiNetwork.construct(self.descMgr)

		codeMappingInfoList=self.genIMMapping()
#		sortedCodeMappingInfoList=codeMappingInfoList
		sortedCodeMappingInfoList=sorted(codeMappingInfoList, key=lambda y: y.getKey())

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
		writer.write(imInfo, sortedCodeMappingInfoList)

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
	oparser.add_option("-i", "--im", "--input-method", dest="input_method", help="輸入法", default="cj")
	oparser.add_option("--format", type="choice", choices=["xml", "yaml", "text", "quiet"], dest="output_format", help="輸出格式，可能的選項有：xml、yaml、text、quiet", default="text")
	oparser.add_option("-q", "--quiet", action="store_true", dest="quiet")
	(options, args) = oparser.parse_args()

	qiangheng=QiangHeng(options)

if __name__ == "__main__":
	main()

