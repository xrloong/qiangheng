from Constant import MainComponentList, MainTemplateFile
from Constant import IMComponentList, IMSubstituteFile, IMRadixList

class CodingConfig:
	def __init__(self, package):
		self.commonComponentFileList = self.getMainComponentList()
		self.commonTemplateFileList = self.getMainTemplateFile()
		self.specificComponentFileList = package.CodingComponentFileList
		self.specificSubstituteFileList = package.CodingSubstituteFileList
		self.specificRadixFileList = package.CodingRadixFileList

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

	def getMainComponentList(self):
		mainDir = self.getMainDir()
		mainComponentList = [
			mainDir + 'CJK.yaml',
			mainDir + 'CJK-A.yaml',
			mainDir + 'component/CJK.yaml',
			mainDir + 'component/CJK-A.yaml',
			mainDir + 'style.yaml',
		]
		return mainComponentList

	def getMainTemplateFile(self):
		mainDir = self.getMainDir()
		mainTemplateFileList = [
			mainDir + 'template.yaml'
		]
		return mainTemplateFileList

	def getMainDir(self):
		return "gen/qhdata/main/"

