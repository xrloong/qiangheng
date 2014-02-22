import sys
from ..CodeInfo.FCCodeInfo import FCCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear import Operator

class FCCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=FCCodeInfo(propDict, codeVariance)
		return codeInfo

	def setByComps(self, codeInfo, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: len(x.getCharacterCode())==4, codeInfoList))
		if isAllWithCode:
			if Operator.OperatorTurtle.equals(operator):
				codeInfo.setCode('Z', 'Z', 'Z', 'Z')
			elif Operator.OperatorEqual.equals(operator):
				targetCodeInfo=codeInfoList[0]
				codeInfo.setCode(
					targetCodeInfo.getTopLeft(),
					targetCodeInfo.getTopRight(),
					targetCodeInfo.getBottomLeft(),
					targetCodeInfo.getBottomRight())
			elif Operator.OperatorEast.equals(operator):
				firstCodeInfo=codeInfoList[0]
				lastCodeInfo=codeInfoList[-1]
				codeInfo.setCode(
					firstCodeInfo.getTopLeft(),
					firstCodeInfo.getTopRight(),
					lastCodeInfo.getBottomLeft(),
					lastCodeInfo.getBottomRight())
			elif Operator.OperatorLoong.equals(operator):
				firstCodeInfo=codeInfoList[0]
				lastCodeInfo=codeInfoList[-1]
				codeInfo.setCode(
					firstCodeInfo.getTopLeft(),
					firstCodeInfo.getTopRight(),
					lastCodeInfo.getBottomLeft(),
					lastCodeInfo.getBottomRight())
			elif Operator.OperatorLoop.equals(operator):
				firstCodeInfo=codeInfoList[0]
				lastCodeInfo=codeInfoList[-1]
				codeInfo.setCode(
					firstCodeInfo.getTopLeft(),
					firstCodeInfo.getTopRight(),
					lastCodeInfo.getBottomLeft(),
					lastCodeInfo.getBottomRight())
			elif Operator.OperatorSilkworm.equals(operator):
				firstCodeInfo=codeInfoList[0]
				lastCodeInfo=codeInfoList[-1]
				codeInfo.setCode(
					firstCodeInfo.getTopLeft(),
					firstCodeInfo.getTopRight(),
					lastCodeInfo.getBottomLeft(),
					lastCodeInfo.getBottomRight())
			elif Operator.OperatorGoose.equals(operator):
				firstCodeInfo=codeInfoList[0]
				lastCodeInfo=codeInfoList[-1]
				codeInfo.setCode(
					firstCodeInfo.getTopLeft(),
					lastCodeInfo.getTopRight(),
					firstCodeInfo.getBottomLeft(),
					lastCodeInfo.getBottomRight())
			else:
				codeInfo.setCode('Z', 'Z', 'Z', 'Z')

