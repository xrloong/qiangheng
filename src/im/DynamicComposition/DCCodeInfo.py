from ..base.CodeInfo import CodeInfo

class DCCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList, region):
		CodeInfo.__init__(self)

		self.strokeList=strokeList
#		self.width, self.height=size
		[left, top, right, bottom]=region
		self.left=left
		self.top=top
		self.right=right
		self.bottomm=bottom

	@staticmethod
	def generateDefaultCodeInfo(strokeList, region=[0, 0, 0xFF, 0xFF]):
		codeInfo=DCCodeInfo(strokeList, region)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeList

	def getCode(self):
		codeList=[stroke.getCode() for stroke in self.strokeList]
		return ','.join(codeList)

