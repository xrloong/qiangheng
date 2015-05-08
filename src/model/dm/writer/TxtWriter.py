from .BaseDmWriter import BaseDmWriter

class TxtWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList))
		print(table)

