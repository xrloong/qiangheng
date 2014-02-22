from .CodeInfo import CodeInfo

class CJCodeInfo(CodeInfo):
	def setPropDict(self, propDict):
		self._cj_single=propDict.get('獨體編碼')
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setCJProp('*', [str_rtlist])

	def setByComps(self, operator, complist):
		# 計算倉頡碼時，需要知道此字的組成方向
		direction=operator.getDirection()

		ansRadixList=[]
		for tmpCodeInfo in complist:
			tmpDirCode, tmpRadixList=tmpCodeInfo.getCJProp()
#			if tmpDirCode=='*':
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

		self.setCJProp(direction, ansRadixList)

	@property
	def code(self):
		if self._cj_single:
			return self._cj_single
		else:
			return CJCodeInfo.computeTotalCode(self._cj_radix_list, self._cj_direction).lower()

	def setDataEmpty(self):
		self._cj_radix_list=None
		self._cj_direction=None
		self._cj_body=None

	def setSingleDataEmpty(self):
		self._cj_single=None

	def setCJProp(self, dir_code, codeList):
		if dir_code!=None and codeList!=None:
			self._cj_radix_list=codeList
			self._cj_direction=dir_code
			self._cj_body=self.computeBodyCode(self._cj_radix_list, dir_code)

	def getCJProp(self):
		return [self._cj_direction, self._cj_radix_list]

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
		headCode=CJCodeInfo.computeHeadTailCode(code, 1)
		return headCode

	@staticmethod
	def computeBodyCode(codeList, direction):
		def convertAllToHeadTail(l):
			pass

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

