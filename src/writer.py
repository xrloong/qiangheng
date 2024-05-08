import ruamel.yaml
import sys

# base writer
class BaseWriter:
	def write(self, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(codeMappingInfoList)

	def writeCodeMapping(self, codeMappingInfoList):
		pass

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table


# quiet writer
class QuietWriter(BaseWriter):
	def writeCodeMapping(self, codeMappingInfoList):
		pass

# quiet writer
class CmYamlWriter(BaseWriter):
	def __init__(self, codeMappingInfoInterpreter, yaml: ruamel.yaml.YAML):
		super().__init__()
		self.codeMappingInfoInterpreter = codeMappingInfoInterpreter

		self.yaml = yaml

	def writeCodeMapping(self, codeMappingInfoList):
		codingTypeName = self.codeMappingInfoInterpreter.getCodingTypeName()

		nodeCodeMaps = []
		for codeMappingInfo in codeMappingInfoList:
			info = self.codeMappingInfoInterpreter.interpreteCodeMappingInfo(codeMappingInfo)
			nodeCodeMaps.append(info)

		codeMappingSet = {
			"編碼類型": codingTypeName,
			"編碼集": nodeCodeMaps
		}

		output = sys.stdout
		self.yaml.dump(codeMappingSet, output)
		print(file = output)

