#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import inject
from injector import Injector

from injection.key import Writer
from injection.key import Characters

from coding.Base import CodeMappingInfoInterpreter

from hanzi.converter import ConstructCharacter
from hanzi.converter import ComputeCharacter

class MainManager:
	@inject
	def __init__(self, injector: Injector):
		self.__injector = injector

	def work(self):
		characterInfos = self.__compute()
		self.__write(characterInfos)

	def __compute(self):
		injector = self.__injector

		characters = injector.get(Characters)
		constructCharacter = injector.get(ConstructCharacter)
		computeCharacter = injector.get(ComputeCharacter)

		characters = sorted(characters)

		constructCharacter.compute(characters)
		characterInfos = computeCharacter.compute(characters)

		return characterInfos

	def __write(self, characterInfos):
		injector = self.__injector

		codeMappingInfoInterpreter = injector.get(CodeMappingInfoInterpreter)
		writer = injector.get(Writer)
		writer.write(characterInfos, codeMappingInfoInterpreter)

