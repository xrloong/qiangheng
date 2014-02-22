from gear.CodeInfoEncoder import CodeInfoEncoder

class CJCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def setByComps(self, codeInfo, operator, codeInfoList):
		# 計算倉頡碼時，需要知道此字的組成方向
		direction=operator.getDirection()

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

