from ..CodeInfo.CJCodeInfo import CJCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class CJCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=CJCodeInfo(propDict, codeVariance)

		direction='*'
		rtlist=codeInfo.getRtList()
		cjBody=self.computeBodyCode(rtlist, direction)
		cjTotal=CJCodeInfoEncoder.computeTotalCode(rtlist, direction).lower()
		codeInfo.setCharacter(cjTotal, cjBody)

		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		return True

	def encodeInternal(self, codeInfo, direction, codeInfoList):
		ansRadixList=[]
		for tmpCodeInfo in codeInfoList:
			tmpDirCode, tmpRadixList=tmpCodeInfo.getCJProp()
			if direction=='$':
				ansRadixList.extend(tmpRadixList)
			elif tmpDirCode in ['*', '@']:
				ansRadixList.append(tmpCodeInfo._cj_body)
			elif tmpDirCode==direction:
				# 同向
				ansRadixList.extend(tmpRadixList)
			else:
				# 不同向
				ansRadixList.append(tmpCodeInfo._cj_body)

		codeInfo.setCJProp(direction, ansRadixList)

		if direction!=None and ansRadixList!=None:
			cjBody=self.computeBodyCode(ansRadixList, direction)
			cjTotal=CJCodeInfoEncoder.computeTotalCode(ansRadixList, direction).lower()
			codeInfo.setCharacter(cjTotal, cjBody)


	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeInternal(codeInfo, '*', codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """
		self.encodeInternal(codeInfo, '*', codeInfoList)

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeInternal(codeInfo, '$', codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeInternal(codeInfo, '*', codeInfoList)


	def encodeAsSilkworm(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '|', codeInfoList)

	def encodeAsGoose(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '-', codeInfoList)

	def encodeAsLoop(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '@', codeInfoList)


	def encodeAsMu(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '$', codeInfoList)

	def encodeAsZuo(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '$', codeInfoList)

	def encodeAsJia(self, codeInfo, codeInfoList):
		self.encodeInternal(codeInfo, '$', codeInfoList)

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
	def computeHeadCode(code):
		headCode=CJCodeInfoEncoder.computeHeadTailCode(code, 1)
		return headCode

	@staticmethod
	def computeBodyCode(codeList, direction):
		def convertAllToHeadTail(l):
			pass

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
