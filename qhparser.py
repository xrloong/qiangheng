#!/usr/bin/env python3

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
			if ch==" ":
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
		self.tokenList.insert(0, token)

	def test(self):
		print("Begin Lexer Test")
		while True:
			t=self.getNextToken()
			if t.ttype==Token.none: break
			else: print(t, end='\t')
		print("\nEnd Lexer Test")

if __name__=='__main__':
	Lexer('(龜)').test()
	Lexer('(好 女子)').test()
	Lexer('(志 土心)').test()
	Lexer('(林 木)').test()
	Lexer('(爻 乂)').test()
	Lexer('(怡 木[流右]皿)').test()
	Lexer('({範贏} 貝)').test()

