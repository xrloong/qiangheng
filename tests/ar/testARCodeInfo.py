from coding.Array.Array import ARCodeInfo

import unittest

class ARCodeInfoTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testPrecoditions(self):
		pass

	def testArray(self):
		# 一
		codeInfo=ARCodeInfo(['1-'])
		self.assertEqual(codeInfo.code, 'a')

		# 丁
		codeInfo=ARCodeInfo(['1-', '3-'])
		self.assertEqual(codeInfo.code, 'ad')

		# 丐
		codeInfo=ARCodeInfo(['1-', '3^', '5-'])
		self.assertEqual(codeInfo.code, 'aeg')

		# 丏
		codeInfo=ARCodeInfo(['1-', '3-', '2-', '5-'])
		self.assertEqual(codeInfo.code, 'adsg')

		# 噩
		codeInfo=ARCodeInfo(['1^', '0-', '4^', '0-', '0-'])
		self.assertEqual(codeInfo.code, 'q;r;')

