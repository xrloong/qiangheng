#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import inject

from injection.key import Writer
from injection.key import Characters

from coding.Base import CodeMappingInfoInterpreter

from hanzi.network import HanZiNetwork
from hanzi.converter import ComputeCharacterInfo
from hanzi.helper import HanZiInterpreter

class MainManager:
	@inject
	def __init__(self,
			hanziNetwork: HanZiNetwork,
			computeCharacterInfo: ComputeCharacterInfo,
			hanziInterpreter: HanZiInterpreter,
			codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
			writer: Writer,
			characters: Characters):
		self.hanziNetwork = hanziNetwork
		self.computeCharacterInfo = computeCharacterInfo
		self.hanziInterpreter = hanziInterpreter
		self.codeMappingInfoInterpreter = codeMappingInfoInterpreter
		self.writer = writer

		self.characters = characters

	def work(self):
		self.compute()
		self.write()

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

