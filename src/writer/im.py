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

class CustomDumper(yaml.Dumper):
	#Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
	def represent_dict_preserve_order(self, data):
		return self.represent_dict(data.items())

CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

class YamlWriter(BaseImWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		nodeNames = {
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
#				"SG":imInfo.getName('sg'),
				}

		# 屬性
		properties = {
				"最大按鍵數": "%s"%imInfo.getMaxKeyLength()
			}

                # 按鍵與顯示的對照表
		nodeKeyMaps = []
		keyMaps = imInfo.getKeyMaps()
		for key, disp in keyMaps:
			attrib = {"按鍵對應": {"按鍵":key, "顯示":disp} }
			nodeKeyMaps.append(attrib)

		nodeCodeMaps = []
		for x in codeMappingInfoList:
			attrib = {"按鍵序列":x.getCode(), "字符":x.getName(), "類型":x.getVariance()}
			nodeCodeMaps.append(attrib)

		r = {
			"輸入法名稱": nodeNames,
			"屬性": properties,
			"按鍵對應集": nodeKeyMaps,
			"對應集": nodeCodeMaps
		}
		print(yaml.dump(r, allow_unicode=True, Dumper = CustomDumper))

if __name__=='__main__':
	pass

