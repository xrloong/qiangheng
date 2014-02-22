import sys

from description.CharacterDescription import CharacterDescription
from description.StructureDescription import HangerStructureDescription
from description.StructureDescription import TurtleStructureDescription
from description.TemplateDescription import TemplateDescription
from description.TemplateDescription import TemplateCondition

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription(operator, CompList)
		return structDesc

	def getDesc_Radix(self, node):
		name=node.get("置換")
		structDesc=self.generateStructureDescription()
		structDesc.setExpandName(name)
		return structDesc

	def getDesc_AssembleChar(self, assembleChar):
		structDescList=[]
		filter_lambda=lambda x: x.tag in ["字根", "組字"]
		targetChildNodes=filter(filter_lambda , list(assembleChar))
		for node in targetChildNodes:
			if node.tag=="字根":
				structDesc=self.getDesc_Radix(node)
			elif node.tag=="組字":
				structDesc=self.getDesc_AssembleChar(node)
			else:
				print("getDesc_AssembleChar: 預期外的標籤。", file=sys.stderr)
			structDescList.append(structDesc)

		operatorName=assembleChar.get("運算")
		if operatorName:
			comp=self.generateStructureDescription([operatorName, structDescList])
		else:
			comp=self.generateStructureDescription()

		return comp

	def getDesc_StructureList(self, nodeCharacter):
		assembleCharList=nodeCharacter.findall("組字")
		compList=[]
		for assembleChar in assembleCharList:
			comp=self.getDesc_AssembleChar(assembleChar)

			comp.setStructureProperties(assembleChar.attrib)

			compList.append(comp)
		return compList

	def getDesc_ParameterList(self, nodeParameter):
		parameterList=[]
		targetParameterNodes=nodeParameter.findall("參數")
		for node in targetParameterNodes:
			charName=node.get('名稱')
			parameterList.append(charName)
		return parameterList

	def getDesc_Template_Structure(self, nodeStructure):
		condition=None

		conditionNode=nodeStructure.find("條件式")
		if conditionNode!=None:
			operator=conditionNode.get('運算')
			operand1=conditionNode.get('運算元一')
			operand2=conditionNode.get('運算元二')
			condition=TemplateCondition([operator, operand1, operand2])
		else:
			condition=TemplateCondition()

		assembleChar=nodeStructure.find("組字")
		comp=self.getDesc_AssembleChar(assembleChar)
		return [condition, comp]

	def getDesc_Template(self, nodeTemplate):
		templateName=nodeTemplate.get('名稱')

		parameterNodeList=nodeTemplate.find("參數列")
		parameterNameList=self.getDesc_ParameterList(parameterNodeList)

		replaceInfoList=[]
		structureNodes=nodeTemplate.findall("組字結構")
		for node in structureNodes:
			replaceInfo=self.getDesc_Template_Structure(node)
			replaceInfoList.append(replaceInfo)
		[condition, comp]=replaceInfoList[0]

		return TemplateDescription(templateName, replaceInfoList, parameterNameList)

	def getDesc_TurtleCharacterList(self, nodeCharacter):
		assembleCharList=nodeCharacter.findall("組字")
		infoDictList=[]
		turtleList=[]
		for assembleChar in assembleCharList:
			infoDict=None
			codeInfo=assembleChar.find("編碼資訊")
			if codeInfo is not None:
				infoDict=codeInfo.attrib

			infoDictList.append(infoDict)

			turtle=TurtleStructureDescription(infoDict)
			turtle.setStructureProperties(assembleChar.attrib)

			turtleList.append(turtle)
		return turtleList

	def loadCodeInfoByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")
		turtleInfoList=[]
		for node in targetChildNodes:
			charName=node.get('名稱')
			turtleList=self.getDesc_TurtleCharacterList(node)

			turtleInfoList.append([charName, turtleList, node.attrib])
		return turtleInfoList

	def loadTemplateByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		templateGroupNode=rootNode.find("範本集")
		templateDB={}
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall("範本")
			for node in targetChildNodes:
				templateName=node.get('名稱')
				templateDesc=self.getDesc_Template(node)
				templateDB[templateName]=templateDesc
		return templateDB

	def loadCharDescriptionByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")

		nodeInfoList=[]
		for node in targetChildNodes:
			structureList=self.getDesc_StructureList(node)
			charName=node.get('名稱')
			charProperties=node.attrib

			charDesc=CharacterDescription(charName)
			charDesc.setStructureList(structureList)
			charDesc.updateProperty(charProperties)

			nodeInfoList.append(charDesc)
		return nodeInfoList

	def loadCodeInfoByParsingXML(self, node):
		version=node.get('版本號')
		propertyDB={}
		if version=='0.2':
			propertyDB=self.loadCodeInfoByParsingXML__0_2(node)
		return propertyDB

	def loadTemplateByParsingXML(self, node):
		version=node.get('版本號')
		templateDB={}
		if version=='0.2':
			templateDB=self.loadTemplateByParsingXML__0_2(node)
		return templateDB

	def loadCharDescriptionByParsingXML(self, node):
		version=node.get('版本號')
		nodeInfoList=[]
		if version=='0.2':
			nodeInfoList=self.loadCharDescriptionByParsingXML__0_2(node)
		return nodeInfoList

