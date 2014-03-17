
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

t_NAME		= r'[一-龥\[\]][一-龥\[\]]*'
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

class TreeRegExp:
	def __init__(self):
		self.children = []
		self.prop={}

		self.flagWithStar = False
		self.flagIsDot = False

		self.matched=[]

	def __str__(self):
		return "%s"%self.prop

	@staticmethod
	def generateDot():
		tre=TreeRegExp()
		tre.setAsDot()
		return tre

	def updateProp(self, prop):
		self.prop.update(prop)

	def setChildren(self, children):
		self.children=children


	def setAsDot(self):
		self.flagIsDot = True

	def setWithStar(self):
		self.flagWithStar = True

	def isWithStar(self):
		return self.flagWithStar

	def isDot(self):
		return self.flagIsDot

	def setMatched(self, matched):
		self.matched = matched

	def getMatched(self):
		return self.matched

class MatchResult:
	def __init__(self):
		self.result=False
		self.matched={}

	def setTrue(self):
		self.result=True

	def setFalse(self):
		self.result=False

	def isMatched(self):
		return self.result

class TreeProxy:
	def __init__(self):
		pass

	def getChildren(self, tree):
		return []

	def matchSingle(self, tre, tree):
		return True

class BasicTreeProxy:
	def __init__(self):
		pass

	def getChildren(self, tree):
		return tree.get("children", [])

	def matchSingle(self, tre, tree):
		prop=tre.prop

		isMatch = True
		if "名稱" in prop:
			isMatch &= prop.get("名稱") == tree.get("name")

		if "運算" in prop:
			isMatch &= prop.get("運算") == tree.get("operator")

		return isMatch

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
yacc.yacc()

def compile(tre):
	root=yacc.parse(tre)
	return root

def match(tre, node, proxy):
	return matchTree(tre, node, proxy)

def matchTree(tre, node, proxy):
	result1=matchNode(tre, node, proxy)
	result2=matchChildren(tre, node, proxy)

	result=MatchResult()
	if result1 and result2.isMatched():
		tre.setMatched([node])
		result.setTrue()
	else:
		tre.setMatched([])
		result.setFalse()
	return result

def matchNode(tre, node, proxy):
	return proxy.matchSingle(tre, node)
	
def matchChildren(tre, node, proxy):
	re_list = tre.children
	node_list = proxy.getChildren(node)

	return matchList(re_list, node_list, proxy)

def matchList(treList, nodeList, proxy):
	if len(treList)==0 and len(nodeList)==0:
		result=MatchResult()
		result.setTrue()
		return result

	if len(treList)>0 and treList[0].isWithStar():
		targetTre=treList[0]
		return matchStar(treList[1:], nodeList, targetTre, proxy)

	if len(treList)>0 and len(nodeList)>0:
		r=treList[0]
		n=nodeList[0]
		result=matchTree(r, n, proxy)
		if r.isDot() or result.isMatched():
			r.setMatched([n])
			return matchList(treList[1:], nodeList[1:], proxy)
	result=MatchResult()
	result.setFalse()
	return result

def matchStar(treList, nodeList, targetTre, proxy):
	index=0
	while index < len(nodeList):
		node=nodeList[index]
		if matchTree(targetTre, node, proxy):
			pass
		else:
			break
		index+=1

	while index>=0:
		result=matchList(treList, nodeList[index:], proxy)
		if result.isMatched():
			result=MatchResult()
			targetTre.setMatched(list(nodeList[:index]))
			result.setTrue()
			return result
		index-=1

	result=MatchResult()
	result.setFalse()
	return result

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

