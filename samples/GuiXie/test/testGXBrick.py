import unittest

from coding.GuiXie.constant import GXStroke, GXCorner
from coding.GuiXie.item import GXBrick

class GXBrickTestCase(unittest.TestCase):
	def setUp(self):
		self.brickStroke = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke2)

		self.brickStroke0 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke0)
		self.brickStroke1 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke1)
		self.brickStroke2 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke2)
		self.brickStroke3 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke3)
		self.brickStroke4 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke4)
		self.brickStroke5 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke5)
		self.brickStroke6 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke6)
		self.brickStroke7 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke7)
		self.brickStroke8 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke8)
		self.brickStroke9 = GXBrick.instanceForStroke(GXCorner.TopLeft, GXStroke.Stroke9)

		self.brickInvalidate = GXBrick.instanceForInvalidate()
		self.brickReference = GXBrick.instanceForReference(GXCorner.TopLeft, self.brickStroke)

	def tearDown(self):
		pass

	def test_isInvalidate(self):
		self.assertTrue(self.brickInvalidate.isInvalidate())
		self.assertFalse(self.brickStroke.isInvalidate())
		self.assertFalse(self.brickReference.isInvalidate())

	def test_isStroke(self):
		self.assertFalse(self.brickInvalidate.isStroke())
		self.assertTrue(self.brickStroke.isStroke())
		self.assertFalse(self.brickReference.isStroke())

	def test_isReference(self):
		self.assertFalse(self.brickInvalidate.isReference())
		self.assertFalse(self.brickStroke.isReference())
		self.assertTrue(self.brickReference.isReference())

	def test_getStroke(self):
		self.assertEqual(self.brickStroke0.getStroke(), GXStroke.Stroke0)
		self.assertEqual(self.brickStroke1.getStroke(), GXStroke.Stroke1)
		self.assertEqual(self.brickStroke2.getStroke(), GXStroke.Stroke2)
		self.assertEqual(self.brickStroke3.getStroke(), GXStroke.Stroke3)
		self.assertEqual(self.brickStroke4.getStroke(), GXStroke.Stroke4)
		self.assertEqual(self.brickStroke5.getStroke(), GXStroke.Stroke5)
		self.assertEqual(self.brickStroke6.getStroke(), GXStroke.Stroke6)
		self.assertEqual(self.brickStroke7.getStroke(), GXStroke.Stroke7)
		self.assertEqual(self.brickStroke8.getStroke(), GXStroke.Stroke8)
		self.assertEqual(self.brickStroke9.getStroke(), GXStroke.Stroke9)

		self.assertEqual(self.brickInvalidate.getStroke(), GXStroke.StrokeNone)


		brickReference3 = GXBrick.instanceForReference(GXCorner.TopLeft, self.brickStroke3)
		self.assertEqual(brickReference3.getStroke(), GXStroke.Stroke3)

		brickReference8 = GXBrick.instanceForReference(GXCorner.TopLeft, self.brickStroke8)
		self.assertEqual(brickReference8.getStroke(), GXStroke.Stroke8)

		brickReferenceInvalidate = GXBrick.instanceForReference(GXCorner.TopLeft, self.brickInvalidate)
		self.assertEqual(brickReferenceInvalidate.getStroke(), GXStroke.StrokeNone)

		brickReferenceOfReference8 = GXBrick.instanceForReference(GXCorner.TopLeft, brickReference8)
		self.assertEqual(brickReferenceOfReference8.getStroke(), GXStroke.Stroke8)

	def test_isUsed(self):
		self.assertFalse(self.brickStroke2.isUsed())
		self.brickStroke2.setUsedByCorner(GXCorner.TopLeft)
		self.assertTrue(self.brickStroke2.isUsed())

		brickReference3 = GXBrick.instanceForReference(GXCorner.TopLeft, self.brickStroke3)
		self.assertFalse(self.brickStroke3.isUsed())
		self.assertFalse(brickReference3.isUsed())
		brickReference3.setUsedByCorner(GXCorner.TopLeft)
		self.assertTrue(self.brickStroke3.isUsed())
		self.assertTrue(brickReference3.isUsed())

