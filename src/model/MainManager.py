#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import inject

from injection.key import Writer
from injection.key import Characters

from coding.Base import CodeMappingInfoInterpreter

from hanzi.converter import ConstructCharacter
from hanzi.converter import ComputeCharacter

class MainManager:
	@inject
	def __init__(self,
			characters: Characters,
			constructCharacter: ConstructCharacter,
			computeCharacter: ComputeCharacter,
			codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
			writer: Writer,
			):
		self.__characters = characters

		self.__constructCharacter = constructCharacter
		self.__computeCharacter = computeCharacter
		self.__codeMappingInfoInterpreter = codeMappingInfoInterpreter
		self.__writer = writer

	def work(self):
		self.__compute()
		self.__write()

	def __compute(self):
		self.__constructCharacter.compute(self.__characters)
		self.__constructCharacter.appendFastCodes()

	def __write(self):
		characterInfos = self.__computeCharacter.compute(self.__characters)
		characterInfos = tuple(sorted(characterInfos, key=lambda c: c.character))

		self.__writer.write(characterInfos, self.__codeMappingInfoInterpreter)

