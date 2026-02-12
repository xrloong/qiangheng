import ruamel.yaml
import sys
from itertools import chain

from coding.Base import CodeMappingInfoInterpreter


# base writer
class BaseWriter:
    def write(
        self, characterInfoList, codeMappingInfoInterpreter: CodeMappingInfoInterpreter
    ):
        codeMappingInfoList = self.genIMMapping(characterInfoList)
        self.writeCodeMapping(codeMappingInfoList, codeMappingInfoInterpreter)

    def writeCodeMapping(
        self,
        codeMappingInfoList,
        codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
    ):
        pass

    def genIMMapping(self, characterInfoList):
        return list(chain.from_iterable(
            characterInfo.codeMappingInfos for characterInfo in characterInfoList
        ))


# quiet writer
class QuietWriter(BaseWriter):
    def writeCodeMapping(
        self,
        codeMappingInfoList,
        codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
    ):
        pass


# YAML writer
class CmYamlWriter(BaseWriter):
    def __init__(self, yaml: ruamel.yaml.YAML):
        super().__init__()
        self.yaml = yaml

    def writeCodeMapping(
        self,
        codeMappingInfoList,
        codeMappingInfoInterpreter: CodeMappingInfoInterpreter,
    ):
        codingTypeName = codeMappingInfoInterpreter.getCodingTypeName()

        nodeCodeMaps = [
            codeMappingInfoInterpreter.interpretCodeMappingInfo(codeMappingInfo)
            for codeMappingInfo in codeMappingInfoList
        ]

        codeMappingSet = {"編碼類型": codingTypeName, "編碼集": nodeCodeMaps}

        output = sys.stdout
        self.yaml.dump(codeMappingSet, output)
        print(file=output)
