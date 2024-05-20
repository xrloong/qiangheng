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
			characters: Characters,
			hanziNetwork: HanZiNetwork,
			computeCharacterInfo: ComputeCharacterInfo,
			hanziInterpreter: HanZiInterpreter,
			codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
			writer: Writer,
			):
		self.__characters = characters

		self.__hanziNetwork = hanziNetwork
		self.__computeCharacterInfo = computeCharacterInfo
		self.__hanziInterpreter = hanziInterpreter
		self.__codeMappingInfoInterpreter = codeMappingInfoInterpreter
		self.__writer = writer

	def work(self):
		self.__compute()
		self.__write()

	def __compute(self):
		self.__computeCharacterInfo.compute(self.__characters)
		self.__computeCharacterInfo.appendFastCodes()

	def __write(self):
		characterInfos = []
		for character in self.__characters:
			charNode = self.__hanziNetwork.findNode(character)
			if charNode:
				characterInfo = self.__hanziInterpreter.interpretCharacterInfo(charNode)
				characterInfos.append(characterInfo)
		characterInfos = tuple(sorted(characterInfos, key=lambda c: c.character))

		self.__writer.write(characterInfos, self.__codeMappingInfoInterpreter)

