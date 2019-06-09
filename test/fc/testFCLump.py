from coding.FourCorner.constant import FCStroke
from coding.FourCorner.constant import FCCorner

from coding.FourCorner.item import FCLump

import unittest

class FCLumpTestCase(unittest.TestCase):
	def setUp(self):
		self.lump1 = FCLump((FCStroke.Stroke3, FCStroke.Stroke5, FCStroke.Stroke8, FCStroke.Stroke4))
		self.lump2 = FCLump((FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft))
		self.lump3 = FCLump((FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCCorner.TopLeft))
		self.lump4 = FCLump((FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCStroke.Stroke5))

	def tearDown(self):
		pass

	def testCorners(self):
		self.assertEqual(self.lump1.corners, (FCStroke.Stroke3, FCStroke.Stroke5, FCStroke.Stroke8, FCStroke.Stroke4))
		self.assertEqual(self.lump2.corners, (FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft))
		self.assertEqual(self.lump3.corners, (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCCorner.TopLeft))
		self.assertEqual(self.lump4.corners, (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCStroke.Stroke5))

