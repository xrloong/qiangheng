#!/usr/bin/env python3

import chardesc

class Token:
	none=0
	space=1
	leftParenthesis=2
	rightParenthesis=3
	variable=4
	hanzi=4
	radical=5
	template=6
	def __init__(self, ttype, value):
		self.ttype=ttype
		self.value=value

	def __str__(self):
		return "({0}:{1})".format(self.ttype, self.value)

Token.tokenNone=Token(Token.none, None)
Token.tokenSpace=Token(Token.space, " ")
Token.tokenLP=Token(Token.leftParenthesis, "(")
Token.tokenRP=Token(Token.rightParenthesis, ")")

def availableHanzi(uchar):
	return 0x4E00 <= ord(uchar) <= 0x9FA6
	return 0x4E00 <= ord(uchar) <= 0x9FBF

class Lexer:
	def __init__(self, data):
		self.data=data
		self.buffer=data
		self.PBTokenList=[]

	def getNextToken(self):
		if len(self.PBTokenList)>0:
			token=self.PBTokenList.pop(0)
		else:
			buffer=self.buffer

			if len(buffer)==0:
				return Token.tokenNone

			token=Token.tokenNone
			ch=buffer[0]
			if ch in [" ", "\t", ]:
				token=Token.tokenSpace
				buffer=buffer[1:]
			elif ch=="(":
				token=Token.tokenLP
				buffer=buffer[1:]
			elif ch==")":
				token=Token.tokenRP
				buffer=buffer[1:]
			elif ch=="[":
				rindex=buffer.find("]")
				if rindex>=0:
					token=Token(Token.radical, "[%s]"%buffer[1:rindex])
				else:
					token=Token.tokenNone
					rindex=0
				buffer=buffer[rindex+1:]
			elif ch=="{":
				rindex=buffer.find("}")
				if rindex>=0:
					token=Token(Token.template, "{%s}"%buffer[1:rindex])
				else:
					token=Token.tokenNone
					rindex=0
				buffer=buffer[rindex+1:]
			elif availableHanzi(ch):
				token=Token(Token.variable, ch)
				buffer=buffer[1:]
			else:
				token=Token.tokenNone
			self.buffer=buffer
		return token

	def pushBackToken(self, token):
		self.PBTokenList.insert(0, token)

	def test(self):
#		print("Begin Lexer Test")
		while True:
			t=self.getNextToken()
			if t.ttype==Token.none: break
			else: print(t, end='\t')
		print()
#		print("End Lexer Test")

class Parser:
	def __init__(self):
		pass

	def parse(data, name=''):
		def parseCompDesc():
			comp=chardesc.CharDesc('王', '(龜)', None)

			tkn=lexer.getNextToken()
			if tkn.ttype != Token.leftParenthesis:
				print("預期 (")
				return chardesc.CharDesc.NoneDesc

			tnk=lexer.getNextToken() # op
			if tnk.ttype == Token.hanzi or tnk.ttype == Token.htemplate:
				comp.setOp(tnk.value)
			else:
				print("預期運算元")
				return chardesc.CharDesc.NoneDesc

			# ' '
			tnk=lexer.getNextToken()
			if tnk.ttype == Token.space:
				while tnk.ttype == Token.space:
					tnk=lexer.getNextToken()
				lexer.pushBackToken(tnk)

				l=parseCompList()

				if l is None:
					return chardesc.CharDesc.NoneDesc
				else:
					comp.setCompList(l)

				tnk=lexer.getNextToken() # ')'
				if tnk.ttype != Token.rightParenthesis:
					print("預期 )")
					return None

			return comp

		def parseCompList():
			l=[]
			while True:
				tnk=lexer.getNextToken()
				if tnk.ttype==Token.hanzi or tnk.ttype==Token.radical:
					comp=chardesc.CharDesc(tnk.value, '龜', None)
					comp.setOp('龜')
					l.append(comp)
				elif tnk.ttype==Token.leftParenthesis:
					lexer.pushBackToken(tnk)
					tmpcomp=parseCompDesc()
					if tmpcomp:
						l.append(tmpcomp)
					else:
						l=None
						break
				else:
					lexer.pushBackToken(tnk)
					break
			return l

		lexer=Lexer(data)
		comp=parseCompDesc()

		if comp!=chardesc.CharDesc.NoneDesc:
			tnk=lexer.getNextToken() # none
			if tnk.ttype == Token.none:
				pass
#				comp.setName(name)
			else:
				print("預期結尾")
				comp=chardesc.CharDesc.NoneDesc

		return comp

	def test():
		descList=[
				'龜)',
				'(龜)',
				'(龜)龍',
				'(好 女子)',
				'(志 (好 木目)心)',
				'(志 雨(好 木目)))',
				'(志 雨好 木目))',
				]
		for d in descList:
			print(d, Parser.parse(d))

	parse=staticmethod(parse)
	test=staticmethod(test)



if __name__=='__main__':
	Lexer('(龜)').test()
	Lexer('(好 女子)').test()
	Lexer('(志 土心)').test()
	Lexer('(林 木)').test()
	Lexer('(爻 乂)').test()
	Lexer('(怡 木[流右]皿)').test()
	Lexer('({範贏} 貝)').test()

	print('=====')

	Parser.test()

