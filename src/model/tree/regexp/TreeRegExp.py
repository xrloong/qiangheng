
tokens = (
	'NAME',
	'PARENTHESIS_LEFT',
	'PARENTHESIS_RIGHT',
	'BRACE_LEFT',
	'BRACE_RIGHT',
	'BACKREF_LEFT',
	'BACKREF_RIGHT',
	'STAR',
#	'QUESTION',
#	'PLUS',
	'DOT',
	'EQUAL',
#	'COMMA',
	)

t_NAME		= r'[一-龥㐀-䶵\[\]][一-龥㐀-䶵\[\]\.0-9]*'
t_PARENTHESIS_LEFT	= r'\('
t_PARENTHESIS_RIGHT	= r'\)'
t_BRACE_LEFT	= r'\{'
t_BRACE_RIGHT	= r'\}'
t_BACKREF_LEFT	= r'\\\('
t_BACKREF_RIGHT	= r'\\\)'
t_STAR	= r'\*'
#t_QUESTION	= r'\?'
#t_PLUS	= r'\+'
t_DOT	= r'\.'
t_EQUAL	= r'='
#t_COMMA	= r','

t_ignore = " \t"

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def p_node(t):
	"""node : PARENTHESIS_LEFT prop PARENTHESIS_RIGHT
		| PARENTHESIS_LEFT prop re_list PARENTHESIS_RIGHT"""
	if len(t)==4:
		current = TreeRegExp()
		current.updateProp(t[2])

		t[0]=current

	if len(t)==5:
		current = TreeRegExp()
		current.updateProp(t[2])
		current.setChildren(t[3])

		t[0]=current

def p_re(t):
	"""re : node
		| DOT
		| re STAR
		| BACKREF_LEFT re_list BACKREF_RIGHT"""
	if len(t)==2:
		if isinstance(t[1], TreeRegExp):
			node=t[1]
			t[0]=node
		else:
			# dot
			token=TreeRegExp.generateDot()
			t[0]=token

	if len(t)==3:
		t[0]=t[1]
		t[0].setWithStar()

def p_re_list(t):
	"""re_list : re
		| re re_list"""
	if len(t)==2:
		t[0]=[t[1]]
	if len(t)==3:
		t[0]=[t[1]]+t[2]

def p_attrib(t):
	'attrib : NAME EQUAL NAME'
	t[0]={t[1]: t[3]}

def p_prop(t):
	"""prop : BRACE_LEFT attrib BRACE_RIGHT
		| BRACE_LEFT BRACE_RIGHT
		|
		"""
	if len(t)==4:
		t[0]=t[2]
	else:
		t[0]={}


def p_error(t):
	print("Syntax error at '%s'" % t.value)

import ply.lex as lex
lexer=lex.lex()
#
import ply.yacc as yacc
parser=yacc.yacc()

def compile(tre):
	root=parser.parse(tre, lexer=lexer)
	return root

from .item import TreeRegExp
from .item import BasicTreeProxy
treeProxy=BasicTreeProxy()

target = {
	"name": "橱",
	"operator": "範好",
	"children": [
		{
			"name": "木",
		},
		{
			"operator": "範廖",
			"name": "厨",
			"children": [
				{
					"name": "厂",
				},
				{
					"name": "[豆寸]",
				},
			]
		},
	]
}

def traverse(root):
	return [root]+sum([traverse(node) for node in root.children], [])

def test(result, target, pattern):
	root=compile(pattern)
	matchResult=match(root, target, treeProxy)
	print(matchResult.isMatched()==result, matchResult.isMatched(), result)

#test(True, target, "({運算=範好} .*)")
#test(True, target, "({運算=範好} ()*)")
#test(True, target, "({} .*)")
#test(True, target, "(.*)")
#test(True, target, "(..)")
#test(False, target, "(.)")
#test(False, target, "(. . .)")

#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=厨}) )")
#test(True, target, "({運算=範好} ({名稱=木}) . )")
#test(False, target, "({運算=範好} . ({名稱=厨}) )")
#test(True, target, "({運算=範好} . . )")
#test(True, target, "({運算=範好} ({名稱=木}) . )")
#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=厨}) ({名稱=厨}) )")
#test(False, target, "({運算=範好} ({名稱=木}) )")

#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=木}) * ({名稱=厨}) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=木}) ({名稱=木}) * ({名稱=厨}) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=火}) * ({名稱=厨}) ({名稱=厂}) * )")
#test(True, target, "({運算=範好} ({名稱=木}) ({名稱=火}) * (({名稱=厂}) .))")
#test(True, target, "({運算=範好} ({名稱=木}) ({名稱=木}) * ({名稱=厨} . .) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=木}) ({名稱=木}) * ({名稱=厨}) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({名稱=木}) ({名稱=木}) * . )")

#test(True, target, "({運算=範好} ({名稱=木}) ({運算=範廖} ({名稱=厂}) ({名稱=[豆寸]}) ) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({運算=範志} ({名稱=厂}) ({名稱=[豆寸]}) ) )")
#test(False, target, "({運算=範好} ({名稱=木}) ({運算=範廖} ({名稱=厂}) ({名稱=豆}) ) )")
#test(True, target, "({運算=範好} ({名稱=木}) ({運算=範廖} . . ) )")
#test(True, target, "({運算=範好} . ({運算=範廖} . . ) )")
#test(True, target, "({運算=範好} . . )")
#test(True, target, "({運算=範好} ({名稱=木}) ( ({名稱=厂}) . ) )")
#test(True, target, "({運算=範好} ({名稱=木}) (. *) )")
#test(True, target, "({運算=範好} . (. .) )")
#test(True, target, "(. (. .) )")
#test(True, target, "({運算=範好} ({名稱=木}) . *)")

#matchResult=match(root, target, treeProxy)
#print(matchResult.isMatched()==result, matchResult.isMatched(), result)

