import yaml
from .BaseImWriter import BaseImWriter

class YamlWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		rootNode="描繪法"

		l=[]
		for x in codeMappingInfoList:
			attrib={"名稱":x.getName(), "描繪序列":x.getCode(), "類型":x.getVariance()}
			l.append(attrib)
		codeMappingSet={"描繪集":l}

		l=[codeMappingSet]
		print(yaml.dump(l, allow_unicode=True))

