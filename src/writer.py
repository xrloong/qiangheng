import ruamel.yaml as yaml

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
	def __init__(self, codeMappingInfoInterpreter):
		super().__init__()
		self.codeMappingInfoInterpreter = codeMappingInfoInterpreter

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

		print(yaml.dump(codeMappingSet, allow_unicode=True, Dumper = CustomDumper))

class CustomDumper(yaml.cyaml.CDumper):
	#Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
	def represent_dict_preserve_order(self, data):
		return self.represent_dict(data.items())

CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

