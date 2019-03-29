from injector import Module
from injector import provider, singleton

from model.base.RadixManager import RadixParser
from model.base.CodeInfoEncoder import CodeInfoEncoder
from model.StructureManager import StructureManager
from model.CharacterDescriptionManager import CharacterDescriptionManager, ImCharacterDescriptionManager
from model.hanzi import HanZiNetwork
import model.base

from Constant import Package, IMName, MethodName
from Constant import MainComponentList, MainTemplateFile
from Constant import IMComponentList, IMSubstituteFile, IMRadixList

class PackageModule(Module):
	@provider
	def provideIMInfo(self, package: Package) -> model.base.IMInfo:
		return package.IMInfo()

	@provider
	def provideCodeInfoEncoder(self, imPackage: Package) -> CodeInfoEncoder:
		return imPackage.CodeInfoEncoder

	@provider
	def provideRadixParser(self, imPackage: Package, imName: IMName, codeInfoEncoder: CodeInfoEncoder) -> RadixParser:
		imRadixParser = imPackage.RadixParser()
		return RadixParser(imName, codeInfoEncoder, imRadixParser)

	@provider
	def provideIMName(self, imInfo: model.base.IMInfo) -> IMName:
		return imInfo.IMName

	@singleton
	@provider
	def provideHanZiNetwork(self) -> HanZiNetwork:
		return HanZiNetwork()

	@provider
	def provideMainComponentList(self) -> MainComponentList:
		mainDir = self.getMainDir()
		mainComponentList = [
			mainDir + 'CJK.yaml',
			mainDir + 'CJK-A.yaml',
			mainDir + 'component/CJK.yaml',
			mainDir + 'component/CJK-A.yaml',
			mainDir + 'style.yaml',
		]
		return mainComponentList

	@provider
	def provideMainTemplateFile(self) -> MainTemplateFile:
		mainDir = self.getMainDir()
		mainTemplateFile = mainDir + 'template.yaml'
		return mainTemplateFile

	@provider
	def provideIMComponentList(self, methodName: MethodName) -> IMComponentList:
		methodDir = self.getMethodDir(methodName)
		methodComponentList = [
			methodDir + 'style.yaml',
		]
		return methodComponentList

	@provider
	def provideIMSubstituteFile(self, methodName: MethodName) -> IMSubstituteFile:
		methodDir = self.getMethodDir(methodName)
		meethodSubstituteFile = methodDir + 'substitute.yaml'
		return meethodSubstituteFile

	@provider
	def provideIMRadixList(self, methodName: MethodName) -> IMRadixList:
		methodDir = self.getMethodDir(methodName)
		methodRadixList = [
			methodDir + 'radix/CJK.yaml',
			methodDir + 'radix/CJK-A.yaml',
			methodDir + 'radix/adjust.yaml'
		]
		return methodRadixList

	def getMainDir(self):
		return "gen/qhdata/main/"

	def getMethodDir(self, methodName):
		return "gen/qhdata/{method}/".format(method=methodName)

