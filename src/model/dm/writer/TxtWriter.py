from .BaseDmWriter import BaseDmWriter

class TxtWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0[0]}\t{0[1]}'.format(x), codeMappingInfoList))
		print(table)

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

