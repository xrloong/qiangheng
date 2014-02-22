from .DCCodeInfo import DCCodeInfo
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.RadixManager import RadixParser
from .Stroke import Stroke
import Constant

class DCRadixParser(RadixParser):
	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		strokeList=[]
		description=infoDict.get('資訊表示式', '')
		region=[0, 0, 0xFF, 0xFF]
		if len(description)>0 and description!='XXXX':
			descriptionList=description.split('|')

			descriptionRegion=descriptionList[0]
			left=int(descriptionRegion[0:2], 16)
			top=int(descriptionRegion[2:4], 16)
			right=int(descriptionRegion[4:6], 16)
			bottom=int(descriptionRegion[6:8], 16)
			region=[left, top, right, bottom]

			description=descriptionList[1]
			strokeDescriptionList=description.split(DCCodeInfo.STROKE_SEPERATOR)
			strokeList=[]
			for d in strokeDescriptionList:
				stroke=Stroke(d, region)
				strokeList.append(stroke)

		codeInfo=self.getEncoder().generateDefaultCodeInfo(strokeList, region)
		return codeInfo

