import ruamel.yaml
import sys

from coding.Base import CodeMappingInfoInterpreter

# base writer
class BaseWriter:
	def write(self, characterInfoList, codeMappingInfoInterpreter: CodeMappingInfoInterpreter):
		codeMappingInfoList = self.genIMMapping(characterInfoList)
		self.writeCodeMapping(codeMappingInfoList, codeMappingInfoInterpreter)

	def writeCodeMapping(self, codeMappingInfoList, codeMappingInfoInterpreter: CodeMappingInfoInterpreter):
		pass

	def genIMMapping(self, characterInfoList):
		table = []
		for characterInfo in characterInfoList:
			table.extend(characterInfo.codeMappingInfos)
		return table


# quiet writer
class QuietWriter(BaseWriter):
	def writeCodeMapping(self, codeMappingInfoList, codeMappingInfoInterpreter: CodeMappingInfoInterpreter):
		pass

# YAML writer
class CmYamlWriter(BaseWriter):
	def __init__(self, yaml: ruamel.yaml.YAML):
		super().__init__()
		self.yaml = yaml

	def writeCodeMapping(self, codeMappingInfoList, codeMappingInfoInterpreter: CodeMappingInfoInterpreter):
		codingTypeName = codeMappingInfoInterpreter.getCodingTypeName()

		nodeCodeMaps = []
		for codeMappingInfo in codeMappingInfoList:
			info = codeMappingInfoInterpreter.interpretCodeMappingInfo(codeMappingInfo)
			nodeCodeMaps.append(info)

		codeMappingSet = {
			"編碼類型": codingTypeName,
			"編碼集": nodeCodeMaps
		}

		output = sys.stdout
		self.yaml.dump(codeMappingSet, output)
		print(file = output)

