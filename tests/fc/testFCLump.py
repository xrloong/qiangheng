from coding.FourCorner.constant import FCStroke
from coding.FourCorner.constant import FCCorner

from coding.FourCorner.item import FCLump

import unittest


class FCLumpTestCase(unittest.TestCase):
    def setUp(self):
        self.lump1 = FCLump(
            (FCStroke.Stroke3, FCStroke.Stroke5, FCStroke.Stroke8, FCStroke.Stroke4)
        )
        self.lump2 = FCLump(
            (FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft)
        )
        self.lump3 = FCLump(
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCCorner.TopLeft)
        )
        self.lump4 = FCLump(
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCStroke.Stroke5)
        )

    def tearDown(self):
        pass

    def testCorners(self):
        self.assertEqual(
            self.lump1.corners,
            (FCStroke.Stroke3, FCStroke.Stroke5, FCStroke.Stroke8, FCStroke.Stroke4),
        )
        self.assertEqual(
            self.lump2.corners,
            (FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft),
        )
        self.assertEqual(
            self.lump3.corners,
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCCorner.TopLeft),
        )
        self.assertEqual(
            self.lump4.corners,
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCStroke.Stroke5),
        )

    def test_computeCodesOfAll(self):
        self.assertEqual(
            self.lump1.computeCodesOfAll(),
            (FCStroke.Stroke3, FCStroke.Stroke5, FCStroke.Stroke8, FCStroke.Stroke4),
        )
        self.assertEqual(
            self.lump2.computeCodesOfAll(),
            (FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft),
        )
        self.assertEqual(
            self.lump3.computeCodesOfAll(),
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCCorner.TopLeft),
        )
        self.assertEqual(
            self.lump4.computeCodesOfAll(),
            (FCStroke.Stroke3, FCCorner.TopLeft, FCCorner.TopLeft, FCStroke.Stroke5),
        )

    def test_computeCodesOfTop(self):
        self.assertEqual(
            self.lump1.computeCodesOfTop(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke5,
            ),
        )
        self.assertEqual(
            self.lump2.computeCodesOfTop(),
            (
                FCStroke.Stroke3,
                FCCorner.TopLeft,
            ),
        )
        self.assertEqual(
            self.lump3.computeCodesOfTop(),
            (
                FCStroke.Stroke3,
                FCCorner.TopLeft,
            ),
        )
        self.assertEqual(
            self.lump4.computeCodesOfTop(),
            (
                FCStroke.Stroke3,
                FCCorner.TopLeft,
            ),
        )

    def test_computeCodesOfBottom(self):
        self.assertEqual(
            self.lump1.computeCodesOfBottom(),
            (
                FCStroke.Stroke8,
                FCStroke.Stroke4,
            ),
        )
        self.assertEqual(
            self.lump2.computeCodesOfBottom(),
            (
                FCStroke.Stroke8,
                FCCorner.BottomLeft,
            ),
        )
        self.assertEqual(
            self.lump3.computeCodesOfBottom(),
            (
                FCStroke.Stroke3,
                FCCorner.BottomLeft,
            ),
        )
        self.assertEqual(
            self.lump4.computeCodesOfBottom(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke5,
            ),
        )

    def test_computeCodesOfLeft(self):
        self.assertEqual(
            self.lump1.computeCodesOfLeft(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke8,
            ),
        )
        self.assertEqual(
            self.lump2.computeCodesOfLeft(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke8,
            ),
        )
        self.assertEqual(
            self.lump3.computeCodesOfLeft(),
            (
                FCStroke.Stroke3,
                FCCorner.TopLeft,
            ),
        )
        self.assertEqual(
            self.lump4.computeCodesOfLeft(),
            (
                FCStroke.Stroke3,
                FCCorner.TopLeft,
            ),
        )

    def test_computeCodesOfRight(self):
        self.assertEqual(
            self.lump1.computeCodesOfRight(),
            (
                FCStroke.Stroke5,
                FCStroke.Stroke4,
            ),
        )
        self.assertEqual(
            self.lump2.computeCodesOfRight(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke8,
            ),
        )
        self.assertEqual(
            self.lump3.computeCodesOfRight(),
            (
                FCStroke.Stroke3,
                FCCorner.TopRight,
            ),
        )
        self.assertEqual(
            self.lump4.computeCodesOfRight(),
            (
                FCStroke.Stroke3,
                FCStroke.Stroke5,
            ),
        )
