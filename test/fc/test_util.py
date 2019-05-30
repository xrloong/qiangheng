import unittest

from coding.FourCorner.constant import FCStroke

from coding.FourCorner import util

class FCUtilTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_convertCharToCornerUnit(self):
		self.assertEqual(util.convertCharToCornerUnit("0"), FCStroke.Stroke0)
		self.assertEqual(util.convertCharToCornerUnit("1"), FCStroke.Stroke1)
		self.assertEqual(util.convertCharToCornerUnit("2"), FCStroke.Stroke2)
		self.assertEqual(util.convertCharToCornerUnit("3"), FCStroke.Stroke3)
		self.assertEqual(util.convertCharToCornerUnit("4"), FCStroke.Stroke4)
		self.assertEqual(util.convertCharToCornerUnit("5"), FCStroke.Stroke5)
		self.assertEqual(util.convertCharToCornerUnit("6"), FCStroke.Stroke6)
		self.assertEqual(util.convertCharToCornerUnit("7"), FCStroke.Stroke7)
		self.assertEqual(util.convertCharToCornerUnit("8"), FCStroke.Stroke8)
		self.assertEqual(util.convertCharToCornerUnit("9"), FCStroke.Stroke9)

	def test_computeCornerUnitCode(self):
		self.assertEqual(util.computeCornerUnitCode(FCStroke.StrokeNone), "0")

		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke0), "0")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke1), "1")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke2), "2")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke3), "3")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke4), "4")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke5), "5")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke6), "6")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke7), "7")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke8), "8")
		self.assertEqual(util.computeCornerUnitCode(FCStroke.Stroke9), "9")
