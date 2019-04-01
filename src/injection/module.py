from injector import Module
from injector import provider

from model.base.CodeInfoEncoder import CodeInfoEncoder
from model.base.IMInfo import IMInfo

from Constant import Package

class PackageModule(Module):
	@provider
	def provideIMInfo(self, package: Package) -> IMInfo:
		return package.IMInfo()

	@provider
	def provideCodeInfoEncoder(self, imPackage: Package) -> CodeInfoEncoder:
		return imPackage.CodeInfoEncoder

