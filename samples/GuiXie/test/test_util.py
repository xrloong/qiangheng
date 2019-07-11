import unittest

from coding.GuiXie.constant import GXGenre
from coding.GuiXie.constant import GXStroke

from coding.GuiXie import util

class GXUtilTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_computeGenreCode(self):
		self.assertEqual(util.computeGenreCode(GXGenre.Zhong), "1")
		self.assertEqual(util.computeGenreCode(GXGenre.Guo), "2")
		self.assertEqual(util.computeGenreCode(GXGenre.Zi), "3")
		self.assertEqual(util.computeGenreCode(GXGenre.Gui), "4")
		self.assertEqual(util.computeGenreCode(GXGenre.Xie), "5")

	def test_computeStrokeCode(self):
		self.assertEqual(util.computeStrokeCode(GXStroke.StrokeNone), "0")

		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke0), "0")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke1), "1")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke2), "2")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke3), "3")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke4), "4")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke5), "5")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke6), "6")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke7), "7")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke8), "8")
		self.assertEqual(util.computeStrokeCode(GXStroke.Stroke9), "9")

	def test_constructCorners(self):
		corners = util.constructCorners("1859")
		self.assertEqual(corners, (GXStroke.Stroke1, GXStroke.Stroke8, GXStroke.Stroke5, GXStroke.Stroke9))

		corners = util.constructCorners("2037")
		self.assertEqual(corners, (GXStroke.Stroke2, GXStroke.Stroke0, GXStroke.Stroke3, GXStroke.Stroke7))

	def test_computeRectCountCode(self):
		self.assertEqual(util.computeRectCountCode(0), "0")
		self.assertEqual(util.computeRectCountCode(3), "3")
		self.assertEqual(util.computeRectCountCode(9), "9")

		self.assertEqual(util.computeRectCountCode(10), "9")
		self.assertEqual(util.computeRectCountCode(12), "9")
		self.assertEqual(util.computeRectCountCode(-3), "0")

