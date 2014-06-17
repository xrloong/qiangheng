import Constant

import ply.lex as lex
import ply.yacc as yacc

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
		comp=_generateNode()
		t[0]=comp

	if len(t)==4:
		prop=t[2]

		name=prop.get(Constant.TAG_REPLACEMENT)
		structDesc=_generateNode()
		structDesc.setReferenceExpression(name)

		t[0]=structDesc

	if len(t)==5:
		prop=t[2]
		structDescList=t[3]

		operatorName=prop.get(Constant.TAG_OPERATOR)
		comp=_generateNode([operatorName, structDescList])

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


def generateNode(self, structInfo=['龜', []]):
	structDesc=structInfo
	return structDesc

_generateNode=generateNode

def parse(expression, g=generateNode):
	global _generateNode
	_generateNode=g
	return parser.parse(expression, lexer=lexer)


lexer=lex.lex()
parser=yacc.yacc()

