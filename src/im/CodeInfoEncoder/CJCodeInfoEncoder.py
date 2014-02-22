from ..CodeInfo.CJCodeInfo import CJCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class CJCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, direction, ansRadixList):
		cjBody=CJCodeInfoEncoder.computeBodyCode(ansRadixList, direction)
		codeInfo=CJCodeInfo(None, direction, ansRadixList, cjBody)

		return codeInfo

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)

		direction='*'
		singleCode=propDict.get('獨體編碼')
		rtlist=[]
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			rtlist=str_rtlist.split(CJCodeInfoEncoder.RADIX_SEPERATOR)

		cjBody=CJCodeInfoEncoder.computeBodyCode(rtlist, direction)
		codeInfo=CJCodeInfo(singleCode, direction, rtlist, cjBody, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def interprettCharacterCode(self, codeInfo):
		singletonCode=codeInfo.getSingletonCode()
		if singletonCode:
			return singletonCode
		else:
			direction=codeInfo.getDirection()
			rtlist=codeInfo.getRtList()

			cjTotal=CJCodeInfoEncoder.computeTotalCode(rtlist, direction).lower()
			return cjTotal

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo


	def encodeAsSilkworm(self, codeInfoList):
		direction='|'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		direction='-'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		direction='@'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo


	def encodeAsMu(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo


	def encodeAsLin(self, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=self.encodeAsLoong([firstCodeInfo])
		bottomCodeInfo=self.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def convertCodeInfoListToRadixList(self, direction, codeInfoList):
		ansRadixList=[]
		for tmpCodeInfo in codeInfoList:
			tmpDirCode=tmpCodeInfo.getDirection()
			tmpRadixList=tmpCodeInfo.getRtList()
			if direction=='$':
				ansRadixList.extend(tmpRadixList)
			elif tmpDirCode in ['*', '@']:
				ansRadixList.append(tmpCodeInfo.getBodyCode())
			elif tmpDirCode==direction:
				# 同向
				ansRadixList.extend(tmpRadixList)
			else:
				# 不同向
				ansRadixList.append(tmpCodeInfo.getBodyCode())

		return ansRadixList

	def encodeAsYin(self, codeInfoList):
		"""運算 "胤" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		if firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_儿:
			radix_丨=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_丨])

			radix_乚=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_乚])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_乚])
			return codeInfo
#		elif firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_丨 and firstCodeInfo.getRtList()[1]==CJCodeInfo.RADIX_丨:
#		elif firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_丨丨:
		elif firstCodeInfo.getRtList()[0]=="l" and firstCodeInfo.getRtList()[1]=="l":
			# work around
			radix_丨=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_丨])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_丨])
			return codeInfo
		else:
			return self.encodeAsInvalidate(codeInfoList)


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
		headCode=CJCodeInfoEncoder.computeHeadTailCode(code, 1)
		return headCode

	@staticmethod
	def computeBodyCode(codeList, direction):
		codeList=CJCodeInfoEncoder.convertRadixListToCodeList(codeList)

		if direction=='$':
			tmpCodeList=[CJCodeInfoEncoder.computeHeadTailCode(x, 3) for x in codeList]
			tmpCode=''.join(tmpCodeList)
			bodyCode=CJCodeInfoEncoder.computeHeadTailCode(tmpCode, 3)
			return bodyCode

		bodyCode=''
		if len(codeList)==0:
			bodyCode=''
		elif len(codeList)==1:
			bodyCode=CJCodeInfoEncoder.computeHeadTailCode(codeList[0], 2)
		else:
			tmpCodeList=codeList

			# 調整特徵碼
			if direction=='@':
				tmpCodeList=codeList[:1]+[CJCodeInfoEncoder.computeHeadCode(x) for x in codeList[1:]]
			else:
				tmpCodeList=[CJCodeInfoEncoder.computeHeadCode(x).lower() for x in codeList[:-1]]+codeList[-1:]

			tmpHeadCode=CJCodeInfoEncoder.computeHeadCode(tmpCodeList[0])
			tmpCodeList=tmpCodeList[1:]

			if len(tmpHeadCode)==2:
				if len(tmpCodeList)>0:
					tmpBodyCode=CJCodeInfoEncoder.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode=''
			elif len(tmpHeadCode)==1:
				tmpHeadCode2=CJCodeInfoEncoder.computeHeadCode(tmpCodeList[0])
				tmpCodeList=tmpCodeList[1:]

				if len(tmpCodeList)>0:
					tmpBodyCode2=CJCodeInfoEncoder.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode2=''
				tmpBodyCode=CJCodeInfoEncoder.computeHeadTailCode(tmpHeadCode2+tmpBodyCode2, 1)
			else:
				# 理論上錯誤
				tmpBodyCode=''
			bodyCode=tmpHeadCode+tmpBodyCode
		return bodyCode

	@staticmethod
	def computeTotalCode(codeList, direction):
		codeList=CJCodeInfoEncoder.convertRadixListToCodeList(codeList)

		if direction=='$':
			totalCode=CJCodeInfoEncoder.computeBodyCode(codeList, direction)
		else:
			if len(codeList)==1:
				totalCode=CJCodeInfoEncoder.computeHeadTailCode(codeList[0], 3)
			elif len(codeList)>1:
				totalCode=CJCodeInfoEncoder.computeHeadCode(codeList[0])+CJCodeInfoEncoder.computeBodyCode(codeList[1:], direction)
			else:
				totalCode=''
		return totalCode

