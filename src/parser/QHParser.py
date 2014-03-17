import sys
import Constant

from description.CharacterDescription import CharacterDescription
from description.StructureDescription import HangerStructureDescription
from description.TemplateDescription import TemplateDescription
from description.TemplateDescription import TemplateSubstitutionDescription

import yaml

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator
		self.g=lambda x=['龜', []]: self.generateStructureDescription(x)

	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def loadTemplateByParsingYAML(self, node):
		templateDB={}
		templateGroupNode=node.get(Constant.TAG_TEMPLATE_SET)
		for node in templateGroupNode:
			templateName=node.get(Constant.TAG_NAME)
			parameterNameList=node.get(Constant.TAG_PARAMETER_LIST)
			structureExpression=node.get(Constant.TAG_STRUCTURE)

			comp=self.parseStructure(structureExpression)
			substitutionList=[TemplateSubstitutionDescription(comp), ]

			templateDesc=TemplateDescription(templateName, parameterNameList, substitutionList)
			templateDB[templateName]=templateDesc
		return templateDB

	def loadTemplates(self, filename):
		node=yaml.load(open(filename), yaml.CLoader)
		return self.loadTemplateByParsingYAML(node)

	def parseStructure(self, structureExpression):
		return parse(structureExpression, self.g)

	def loadCharDescriptionByParsingYAML(self, rootNode):
		charDescList=[]
		charGroupNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for node in charGroupNode:
			charName=node.get(Constant.TAG_NAME)

			charDesc=CharacterDescription(charName)

			if Constant.TAG_STRUCTURE in node:
				structureExpression=node.get(Constant.TAG_STRUCTURE)
				comp=self.parseStructure(structureExpression)
				structureList=[comp, ]
				charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadCharacters(self, filename):
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

t_NAME			= r'[一-龥㐀-䶵\[\]][一-龥㐀-䶵\[\]]*(\.[0-9])?'
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


def p_node(t):
	"""node : PARENTHESIS_LEFT PARENTHESIS_RIGHT
		| PARENTHESIS_LEFT prop node_list PARENTHESIS_RIGHT
		| PARENTHESIS_LEFT prop PARENTHESIS_RIGHT"""
	if len(t)==3:
		comp=_generateStructure()
		t[0]=comp

	if len(t)==4:
		prop=t[2]

		name=prop.get(Constant.TAG_REPLACEMENT)
		structDesc=_generateStructure()
		structDesc.setReferenceExpression(name)

		t[0]=structDesc

	if len(t)==5:
		prop=t[2]
		structDescList=t[3]

		operatorName=prop.get(Constant.TAG_OPERATOR)
		comp=_generateStructure([operatorName, structDescList])

		t[0]=comp

def p_node_list(t):
	"""node_list : node
		| node node_list"""
	if len(t)==2:
		t[0]=[t[1]]
	if len(t)==3:
		t[0]=[t[1]]+t[2]

def p_attrib(t):
	'attrib : NAME EQUAL NAME'
	t[0]={t[1]: t[3]}
#	print(t[1], t[3])

def p_prop(t):
	'prop : BRACE_LEFT attrib BRACE_RIGHT'
	t[0]=t[2]


def p_error(t):
	print("Syntax error at '%s'" % t.value)

def generateStructure(self, structInfo=['龜', []]):
	structDesc=structInfo
	return structDesc

_generateStructure=generateStructure

def parse(expression, g=generateStructure):
	global _generateStructure
	_generateStructure=g
	return yacc.parse(expression)

import ply.lex as lex
lex.lex()

import ply.yacc as yacc
yacc.yacc()

