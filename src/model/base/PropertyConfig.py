from injector import inject

from Constant import MainComponentList, MainTemplateFile
from Constant import IMComponentList, IMSubstituteFile, IMRadixList

class PropertyConfig:
	@inject
	def __init__(self, commonComponentFileList: MainComponentList,
		commonTemplateFile: MainTemplateFile,
		specificComponentFileList: IMComponentList,
		specificSubstituteFile: IMSubstituteFile,
		specificRadixFileList: IMRadixList):

		self.commonComponentFileList = commonComponentFileList
		self.commonTemplateFile = commonTemplateFile
		self.specificComponentFileList = specificComponentFileList
		self.specificSubstituteFile = specificSubstituteFile
		self.specificRadixFileList = specificRadixFileList

	def getCommonComponentFileList(self):
		return self.commonComponentFileList

	def getCommonTemplateFile(self):
		return self.commonTemplateFile

	def getSpecificComponentFileList(self):
		return self.specificComponentFileList

	def getSpecificSubstituteFile(self):
		return self.specificSubstituteFile

	def getSpecificRadixFileList(self):
		return self.specificRadixFileList

