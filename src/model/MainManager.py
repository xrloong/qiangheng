#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import inject
from injector import Injector

from injection.key import Writer
from injection.key import Characters
from injection.key import SeparateComputing

from coding.Base import CodeMappingInfoInterpreter

from hanzi.work import CharacterStructuringWork
from hanzi.work import CharacterCodeAppendingWork
from hanzi.work import CharacterCodeComputingWork


class MainManager:
    @inject
    def __init__(self, injector: Injector):
        self.__injector = injector

    def work(self):
        characterInfos = self.__compute()
        self.__write(characterInfos)

    def __compute(self):
        injector = self.__injector

        structuringWork = injector.get(CharacterStructuringWork)
        appendingWork = injector.get(CharacterCodeAppendingWork)
        computingWork = injector.get(CharacterCodeComputingWork)

        characters = injector.get(Characters)
        separateComputing = injector.get(SeparateComputing)

        structuringWork.setupOnCreateNodeListener()

        characters = sorted(characters)

        characterInfos = []
        for character in characters:
            if separateComputing:
                structuringWork.reset()

            structuringWork.constructCharacter(character)
            appendingWork.appendCodesForAddedCharacters()
            characterInfo = computingWork.computeCharacter(character)
            if characterInfo:
                characterInfos.append(characterInfo)

        return characterInfos

    def __write(self, characterInfos):
        injector = self.__injector

        codeMappingInfoInterpreter = injector.get(CodeMappingInfoInterpreter)
        writer = injector.get(Writer)
        writer.write(characterInfos, codeMappingInfoInterpreter)
