#from xml.etree import ElementTree as ET
from xml.etree import cElementTree as ET
#import lxml.etree as ET
#import lxml.objectify as ET

class ConfigParser:
	def readConfig(self, configFileName):
		xmlNode=ET.parse(configFileName)
		rootNode=xmlNode.getroot()

		configNode=rootNode.find('設定')
		imNode=configNode.find('輸入法')
		imProp=imNode.attrib

#		configFileNode=rootNode.find('設定檔')
		[toTemplateList, toComponentList, toCodeList]=self.getConfigFiles(configFileName)

		return [imProp, toTemplateList, toComponentList, toCodeList]

	def getConfigFiles(self, configFileName):
		xmlNode=ET.parse(configFileName)
		rootNode=xmlNode.getroot()
		configFileNode=rootNode.find('設定檔')

		importNodeList=configFileNode.findall('匯入')

		templateNodeList=configFileNode.findall('範本')
		componentNodeList=configFileNode.findall('部件')
		radixNodeList=configFileNode.findall('字根')

		rootDirPrefix=configFileNode.get('資料目錄')

		toComponentList=[]
		toTemplateList=[]
		toCodeList=[]

		for node in importNodeList:
			fileName=rootDirPrefix+node.get('檔案')
			[tmpToTemplateList, tmpToComponentList, tmpToCodeList]= \
				self.getConfigFiles(fileName)
			toComponentList.extend(tmpToComponentList)
			toTemplateList.extend(tmpToTemplateList)
			toCodeList.extend(tmpToCodeList)

		tmpToComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]
		tmpToTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]
		tmpToCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]

		toComponentList.extend(tmpToComponentList)
		toTemplateList.extend(tmpToTemplateList)
		toCodeList.extend(tmpToCodeList)

		return [toTemplateList, toComponentList, toCodeList]


