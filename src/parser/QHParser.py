import sys
import Constant

from description.CharacterDescription import CharacterDescription
from description.StructureDescription import HangerStructureDescription
from description.TemplateDescription import TemplateDescription
from description.TemplateDescription import TemplateSubstitutionDescription

#from xml.etree import ElementTree as ET
from xml.etree import cElementTree as ET
#import lxml.etree as ET
#import lxml.objectify as ET

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def getDesc_Radix(self, node):
		name=node.get(Constant.TAG_REPLACEMENT)
		structDesc=self.generateStructureDescription()
		structDesc.setReferenceExpression(name)
		return structDesc

	def getDesc_AssembleChar(self, assembleChar):
		structDescList=[]
		filter_lambda=lambda x: x.tag in [Constant.TAG_RADIX, Constant.TAG_COMPOSITION]
#		targetChildNodes=filter(filter_lambda , assembleChar.iterchildren())
		targetChildNodes=filter(filter_lambda , list(assembleChar))
		for node in targetChildNodes:
			if node.tag==Constant.TAG_RADIX:
				structDesc=self.getDesc_Radix(node)
			elif node.tag==Constant.TAG_COMPOSITION:
				structDesc=self.getDesc_AssembleChar(node)
			else:
				print("getDesc_AssembleChar: 預期外的標籤。", file=sys.stderr)
			structDescList.append(structDesc)

		operatorName=assembleChar.get(Constant.TAG_OPERATOR)
		if operatorName:
			comp=self.generateStructureDescription([operatorName, structDescList])
		else:
			comp=self.generateStructureDescription()

		return comp

	def getDesc_StructureList(self, nodeCharacter):
		assembleCharList=nodeCharacter.findall(Constant.TAG_COMPOSITION)
		compList=[]
		for assembleChar in assembleCharList:
			comp=self.getDesc_AssembleChar(assembleChar)

			comp.setStructureProperties(assembleChar.attrib)

			compList.append(comp)
		return compList

	def getDesc_ParameterList(self, nodeParameter):
		parameterList=[]
		targetParameterNodes=nodeParameter.findall(Constant.TAG_PARAMETER)
		for node in targetParameterNodes:
			charName=node.get(Constant.TAG_NAME)
			parameterList.append(charName)
		return parameterList

	def getDesc_Template_Substitution(self, nodeStructure):
		assembleChar=nodeStructure.find(Constant.TAG_COMPOSITION)
		comp=self.getDesc_AssembleChar(assembleChar)
		return TemplateSubstitutionDescription(comp)

	def getDesc_Template(self, nodeTemplate):
		templateName=nodeTemplate.get(Constant.TAG_NAME)

		parameterNodeList=nodeTemplate.find(Constant.TAG_PARAMETER_LIST)
		parameterNameList=self.getDesc_ParameterList(parameterNodeList)

		substitutionList=[]
		structureNodes=nodeTemplate.findall(Constant.TAG_COMPOSITION_STRUCTURE)
		for node in structureNodes:
			substitution=self.getDesc_Template_Substitution(node)
			substitutionList.append(substitution)

		return TemplateDescription(templateName, parameterNameList, substitutionList)

	def loadTemplateByParsingXML__0_3(self, rootNode):
		# 用於 0.3 版
		templateGroupNode=rootNode.find(Constant.TAG_TEMPLATE_SET)
		templateDB={}
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall(Constant.TAG_TEMPLATE)
			for node in targetChildNodes:
				templateName=node.get(Constant.TAG_NAME)
				templateDesc=self.getDesc_Template(node)
				templateDB[templateName]=templateDesc
		return templateDB

	def loadCharDescriptionByParsingXML__0_3(self, rootNode):
		# 用於 0.3 版
		charGroupNode=rootNode.find(Constant.TAG_CHARACTER_SET)
		targetChildNodes=charGroupNode.findall(Constant.TAG_CHARACTER)

		charDescList=[]
		for node in targetChildNodes:
			structureList=self.getDesc_StructureList(node)
			charName=node.get(Constant.TAG_NAME)

			charDesc=CharacterDescription(charName)
			charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadTemplateByParsingXML(self, node):
		version=node.get(Constant.TAG_VERSION)
		templateDB={}
		if version=='0.3':
			templateDB=self.loadTemplateByParsingXML__0_3(node)
		return templateDB

	def loadCharDescriptionByParsingXML(self, node):
		version=node.get(Constant.TAG_VERSION)
		charDescList=[]
		if version=='0.3':
			charDescList=self.loadCharDescriptionByParsingXML__0_3(node)
		return charDescList

	def loadTemplates(self, filename):
		xmlNode=ET.parse(filename)
		rootNode=xmlNode.getroot()
		return self.loadTemplateByParsingXML(rootNode)

	def loadCharacters(self, filename):
		xmlNode=ET.parse(filename)
		rootNode=xmlNode.getroot()
		charDescList=self.loadCharDescriptionByParsingXML(rootNode)
		return charDescList

	def parseStructure(self, structureExpression):
		return parse(self, structureExpression)

	def loadCharDescriptionByParsingYAML(self, rootNode):
		charDescList=[]
		charGroupNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for node in charGroupNode:
			charName=node.get(Constant.TAG_NAME)

			charDesc=CharacterDescription(charName)

			if Constant.TAG_STRUCTURE in node:
				structureExpression=node.get(Constant.TAG_STRUCTURE)
				structureList=self.parseStructure(structureExpression)
				charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadCharactersYAML(self, filename):
		import yaml
		node=yaml.load(open(filename), yaml.CLoader)
		return self.loadCharDescriptionByParsingYAML(node)

tokens = (
	'NAME',
	'PARENTHESIS_LEFT',
	'PARENTHESIS_RIGHT',
	'BRACE_LEFT',
	'BRACE_RIGHT',
#	'STAR',
#	'QUESTION',
#	'PLUS',
#	'DOT',
	'EQUAL',
#	'COMMA',
	)

t_NAME			= r'[一-龥㐀-䶵\[\]][一-龥㐀-䶵\[\]]*'
t_PARENTHESIS_LEFT	= r'\('
t_PARENTHESIS_RIGHT	= r'\)'
t_BRACE_LEFT		= r'\{'
t_BRACE_RIGHT		= r'\}'
#t_STAR			= r'\*'
#t_QUESTION		= r'\?'
#t_PLUS			= r'\+'
#t_DOT			= r'\.'
t_EQUAL			= r'='
#t_COMMA			= r','

t_ignore = " \t"

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


def p_node_list(t):
	"""node_list : node
		| node node_list"""
	if len(t)==2:
		t[0]=[t[1]]
	if len(t)==3:
		t[0]=[t[1]]+t[2]

def p_node(t):
	"""node : PARENTHESIS_LEFT PARENTHESIS_RIGHT
		| PARENTHESIS_LEFT prop node_list PARENTHESIS_RIGHT
		| PARENTHESIS_LEFT prop PARENTHESIS_RIGHT"""
	if len(t)==3:
		comp=parser.generateStructureDescription()
		t[0]=comp

	if len(t)==4:
		prop=t[2]

		name=prop.get(Constant.TAG_REPLACEMENT)
		structDesc=parser.generateStructureDescription()
		structDesc.setReferenceExpression(name)

		t[0]=structDesc

	if len(t)==5:
		prop=t[2]
		structDescList=t[3]

		operatorName=prop.get(Constant.TAG_OPERATOR)
		comp=parser.generateStructureDescription([operatorName, structDescList])

		t[0]=comp

def p_attrib(t):
	'attrib : NAME EQUAL NAME'
	t[0]={t[1]: t[3]}
#	print(t[1], t[3])

def p_prop(t):
	'prop : BRACE_LEFT attrib BRACE_RIGHT'
	t[0]=t[2]


def p_error(t):
	print("Syntax error at '%s'" % t.value)

parser=None
def parse(p, expression):
	global parser
	parser=p
	return yacc.parse(expression)

import ply.lex as lex
lex.lex()

import ply.yacc as yacc
yacc.yacc()

