
from im.base.CodeInfo import CodeInfo
import unittest

class CodeInfoTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testPrecoditions(self):
		pass

	def testDefault(self):
		codeInfo=CodeInfo()
		self.assertIsNotNone(codeInfo)

		self.assertEqual(codeInfo.toCode(), "")

	def testGenerateDefault(self):
		codeInfo=CodeInfo.generateDefaultCodeInfo()
		self.assertIsNotNone(codeInfo)

		self.assertEqual(codeInfo.toCode(), "")

