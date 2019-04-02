from Constant import MainComponentList, MainTemplateFile
from Constant import IMComponentList, IMSubstituteFile, IMRadixList

class CodingConfig:
	def __init__(self, commonComponentFileList: MainComponentList,
		commonTemplateFileList: MainTemplateFile,
		specificComponentFileList: IMComponentList,
		specificSubstituteFileList: IMSubstituteFile,
		specificRadixFileList: IMRadixList):

		self.commonComponentFileList = commonComponentFileList
		self.commonTemplateFileList = commonTemplateFileList
		self.specificComponentFileList = specificComponentFileList
		self.specificSubstituteFileList = specificSubstituteFileList
		self.specificRadixFileList = specificRadixFileList

	def getCommonComponentFileList(self):
		return self.commonComponentFileList

	def getCommonTemplateFileList(self):
		return self.commonTemplateFileList

	def getSpecificComponentFileList(self):
		return self.specificComponentFileList

	def getSpecificSubstituteFileList(self):
		return self.specificSubstituteFileList

	def getSpecificRadixFileList(self):
		return self.specificRadixFileList

