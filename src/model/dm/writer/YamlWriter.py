import yaml
from .BaseDmWriter import BaseDmWriter

class YamlWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		rootNode="描繪法"

		l=[]
		for x in codeMappingInfoList:
			attrib={"名稱":x[0], "描繪序列":x[1]}
			l.append(attrib)
		codeMappingSet={"描繪集":l}

		l=[codeMappingSet]
		print(yaml.dump(l, allow_unicode=True))

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			codeMappingInfoList=characterInfo.getCodeMappingInfoList()
			for codeMappingInfo in codeMappingInfoList:
				code=codeMappingInfo.getCode()
				charName=codeMappingInfo.getName()

				if len(charName)>1:
					continue

				expressionList=[stroke.getExpression() for stroke in code]
				table.append((charName, ";".join(expressionList)))
		return table

