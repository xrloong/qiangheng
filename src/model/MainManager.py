#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from injector import inject
from injector import Injector

from injection.key import Writer
from injection.key import Characters
from injection.key import SeparateComputing

from coding.Base import CodeMappingInfoInterpreter

from hanzi.work import CharacterStructuringWork
from hanzi.work import HanZiCodeInfosComputer


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
        codeInfosComputer = injector.get(HanZiCodeInfosComputer)

        characters = injector.get(Characters)
        separateComputing = injector.get(SeparateComputing)

        characters = sorted(characters)

        characterInfos = []
        for character in characters:
            if separateComputing:
                structuringWork.reset()

            structuringWork.constructCharacter(character)
            structuringWork.appendCodesForAddedNodes()
            characterInfo = codeInfosComputer.computeCharacter(character)
            if characterInfo:
                characterInfos.append(characterInfo)

        return characterInfos

    def __write(self, characterInfos):
        injector = self.__injector

        codeMappingInfoInterpreter = injector.get(CodeMappingInfoInterpreter)
        writer = injector.get(Writer)
        writer.write(characterInfos, codeMappingInfoInterpreter)
