# base writer
class BaseImWriter:
	def write(self, imInfo, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(imInfo, codeMappingInfoList)

	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		pass

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table


# Quiet writer
class QuietWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		pass


# TEXT writer
class TxtWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList))
		print(table)


# XML writer
#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET

class XmlWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ET.Element("輸入法")

		# 名稱
		nameNode=ET.SubElement(rootNode, "輸入法名稱",
			attrib={
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
#				"SG":imInfo.getName('sg'),
				})

		# 屬性
		propertyNode=ET.SubElement(rootNode, "屬性",
			attrib={
				"最大按鍵數":"%s"%imInfo.getMaxKeyLength()
				})

		# 按鍵與顯示的對照表
		keyMapsNode=ET.SubElement(rootNode, "按鍵對應集")
		for key, disp in keyMaps:
			attrib={"按鍵":key, "顯示":disp}
			ET.SubElement(keyMapsNode, "按鍵對應", attrib)

		# 對照表
		charGroup=ET.SubElement(rootNode, "對應集")
		for x in codeMappingInfoList:
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "類型":x.getVariance()}
			ET.SubElement(charGroup, "對應", attrib)
		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")


# YAML writer
import yaml

class YamlWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		rootNode="輸入法"
		nameNode={"輸入法名稱": {
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
				"SG":imInfo.getName('sg'),
				}}

                # 按鍵與顯示的對照表
		l=[]
		keyMaps=imInfo.getKeyMaps()
		for key, disp in keyMaps:
			attrib={"按鍵對應": {"按鍵":key, "顯示":disp} }
			l.append(attrib)
		keyMappingSet={"按鍵對應集":l}

		l=[]
		for x in codeMappingInfoList:
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "類型":x.getVariance()}
			l.append(attrib)
		codeMappingSet={"對應集":l}

		l=[nameNode, keyMappingSet, codeMappingSet]
		print(yaml.dump(l, allow_unicode=True))

if __name__=='__main__':
	pass

