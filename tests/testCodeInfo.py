from coding.Base.Base import CodeInfo
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

		self.assertEqual(codeInfo.code, "")

	def testGenerateDefault(self):
		codeInfo=CodeInfo.generateDefaultCodeInfo()
		self.assertIsNotNone(codeInfo)

		self.assertEqual(codeInfo.code, "")

