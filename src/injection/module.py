from injector import Module
from injector import provider

from model.base.RadixManager import RadixParser
from model.base.CodeInfoEncoder import CodeInfoEncoder
from model.base.IMInfo import IMInfo

from Constant import Package, IMName

class PackageModule(Module):
	@provider
	def provideIMInfo(self, package: Package) -> IMInfo:
		return package.IMInfo()

	@provider
	def provideCodeInfoEncoder(self, imPackage: Package) -> CodeInfoEncoder:
		return imPackage.CodeInfoEncoder

	@provider
	def provideRadixParser(self, imPackage: Package, imName: IMName, codeInfoEncoder: CodeInfoEncoder) -> RadixParser:
		imRadixParser = imPackage.RadixParser()
		return RadixParser(imName, codeInfoEncoder, imRadixParser)

	@provider
	def provideIMName(self, imInfo: IMInfo) -> IMName:
		return imInfo.IMName

