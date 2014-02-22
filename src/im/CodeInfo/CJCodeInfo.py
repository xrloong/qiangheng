from gear.CodeInfo import CodeInfo

class CJCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	RADIX_丨='$丨'
	RADIX_乚='$乚'
	RADIX_丨丨='$丨丨'
	RADIX_儿='$儿'

	radixToCodeDict={
		RADIX_丨:['*', ['l']],
		RADIX_乚:['*', ['u']],
		RADIX_丨丨:['-', ['l', 'l']],
		RADIX_儿:['-', ['h', 'u']],
	}

	def __init__(self, singleCode, direction, radixList, cjBody, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)
		self._cj_single=singleCode


		self._cj_rtlist=radixList
		self._cj_direction=direction
		self._cj_body=cjBody

	@staticmethod
	def generateDefaultCodeInfo(direction, ansRadixList):
		cjBody=CJCodeInfo.computeBodyCode(ansRadixList, direction)
		codeInfo=CJCodeInfo(None, direction, ansRadixList, cjBody)

		return codeInfo

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)

		direction='*'
		singleCode=propDict.get('獨體編碼')
		rtlist=[]
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			rtlist=str_rtlist.split(CJCodeInfo.RADIX_SEPERATOR)

		cjBody=CJCodeInfo.computeBodyCode(rtlist, direction)
		codeInfo=CJCodeInfo(singleCode, direction, rtlist, cjBody, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def toCode(self):
		singletonCode=self.getSingletonCode()
		if singletonCode:
			return singletonCode
		else:
			direction=self.getDirection()
			rtlist=self.getRtList()

			cjTotal=CJCodeInfo.computeTotalCode(rtlist, direction).lower()
			return cjTotal


	def getSingletonCode(self):
		return self._cj_single

	def getDirection(self):
		return self._cj_direction

	def getRtList(self):
		return self._cj_rtlist

	def getSingle(self):
		return self._cj_single

	def getBodyCode(self):
		return self._cj_body


	@staticmethod
	def computeHeadTailCode(code, headCount):
		frontCode=code[:headCount]
		rearCode=code[headCount:]

		# 以大寫來表示重要的尾碼
		xTailCode=list(filter(lambda x: x.isupper(), rearCode))
		if len(xTailCode)>0:
			# 重要的尾碼
			tailCode=xTailCode[-1]
		elif len(rearCode)>0:
			tailCode=rearCode[-1]
		else:
			tailCode=''

		return frontCode+tailCode

	@staticmethod
	def convertRadixListToCodeList(radixList):
		return sum([CJCodeInfo.radixToCodeDict.get(radix, ['*', [radix]])[1] for radix in radixList], [])

	@staticmethod
	def computeHeadCode(code):
		headCode=CJCodeInfo.computeHeadTailCode(code, 1)
		return headCode

	@staticmethod
	def computeBodyCode(codeList, direction):
		codeList=CJCodeInfo.convertRadixListToCodeList(codeList)

		if direction=='$':
			tmpCodeList=[CJCodeInfo.computeHeadTailCode(x, 3) for x in codeList]
			tmpCode=''.join(tmpCodeList)
			bodyCode=CJCodeInfo.computeHeadTailCode(tmpCode, 3)
			return bodyCode

		bodyCode=''
		if len(codeList)==0:
			bodyCode=''
		elif len(codeList)==1:
			bodyCode=CJCodeInfo.computeHeadTailCode(codeList[0], 2)
		else:
			tmpCodeList=codeList

			# 調整特徵碼
			if direction=='@':
				tmpCodeList=codeList[:1]+[CJCodeInfo.computeHeadCode(x) for x in codeList[1:]]
			else:
				tmpCodeList=[CJCodeInfo.computeHeadCode(x).lower() for x in codeList[:-1]]+codeList[-1:]

			tmpHeadCode=CJCodeInfo.computeHeadCode(tmpCodeList[0])
			tmpCodeList=tmpCodeList[1:]

			if len(tmpHeadCode)==2:
				if len(tmpCodeList)>0:
					tmpBodyCode=CJCodeInfo.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode=''
			elif len(tmpHeadCode)==1:
				tmpHeadCode2=CJCodeInfo.computeHeadCode(tmpCodeList[0])
				tmpCodeList=tmpCodeList[1:]

				if len(tmpCodeList)>0:
					tmpBodyCode2=CJCodeInfo.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode2=''
				tmpBodyCode=CJCodeInfo.computeHeadTailCode(tmpHeadCode2+tmpBodyCode2, 1)
			else:
				# 理論上錯誤
				tmpBodyCode=''
			bodyCode=tmpHeadCode+tmpBodyCode
		return bodyCode

	@staticmethod
	def computeTotalCode(codeList, direction):
		codeList=CJCodeInfo.convertRadixListToCodeList(codeList)

		if direction=='$':
			totalCode=CJCodeInfo.computeBodyCode(codeList, direction)
		else:
			if len(codeList)==1:
				totalCode=CJCodeInfo.computeHeadTailCode(codeList[0], 3)
			elif len(codeList)>1:
				totalCode=CJCodeInfo.computeHeadCode(codeList[0])+CJCodeInfo.computeBodyCode(codeList[1:], direction)
			else:
				totalCode=''
		return totalCode

