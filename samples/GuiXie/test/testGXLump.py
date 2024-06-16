import unittest

from coding.GuiXie.constant import GXStroke
from coding.GuiXie.constant import GXCorner
from coding.GuiXie.item import GXLump

from coding.GuiXie import util


class GXLumpTestCase(unittest.TestCase):
    def setUp(self):
        self.gxLump = GXLump(util.constructCorners("2593"))

    def tearDown(self):
        pass

    def test_corners(self):
        self.assertEqual(self.gxLump.topLeft.getStroke(), GXStroke.Stroke2)
        self.assertEqual(self.gxLump.topRight.getStroke(), GXStroke.Stroke5)
        self.assertEqual(self.gxLump.bottomLeft.getStroke(), GXStroke.Stroke9)
        self.assertEqual(self.gxLump.bottomRight.getStroke(), GXStroke.Stroke3)

    def test_computeStrokes(self):
        # single corner
        self.assertEqual(
            self.gxLump.computeStrokes((GXCorner.TopLeft,)), [GXStroke.Stroke2]
        )
        self.assertEqual(
            self.gxLump.computeStrokes((GXCorner.TopRight,)), [GXStroke.Stroke5]
        )
        self.assertEqual(
            self.gxLump.computeStrokes((GXCorner.BottomLeft,)), [GXStroke.Stroke9]
        )
        self.assertEqual(
            self.gxLump.computeStrokes((GXCorner.BottomRight,)), [GXStroke.Stroke3]
        )

        # multiple corners
        self.assertEqual(
            self.gxLump.computeStrokes(
                (
                    GXCorner.TopLeft,
                    GXCorner.BottomLeft,
                )
            ),
            [
                GXStroke.Stroke2,
                GXStroke.Stroke9,
            ],
        )

        # multiple corners with custom order
        cornersWithCustomOrder = (
            GXCorner.BottomLeft,
            GXCorner.TopRight,
            GXCorner.TopLeft,
            GXCorner.BottomRight,
        )
        self.assertEqual(
            self.gxLump.computeStrokes(cornersWithCustomOrder),
            [
                GXStroke.Stroke9,
                GXStroke.Stroke5,
                GXStroke.Stroke2,
                GXStroke.Stroke3,
            ],
        )

        # multiple corners with duplicated corners
        cornersWithCustomOrder = (
            GXCorner.BottomLeft,
            GXCorner.TopRight,
            GXCorner.BottomLeft,
        )
        self.assertEqual(
            self.gxLump.computeStrokes(cornersWithCustomOrder),
            [
                GXStroke.Stroke9,
                GXStroke.Stroke5,
                GXStroke.StrokeNone,
            ],
        )

    def test_computeStrokesOnAllCorners(self):
        self.assertEqual(
            self.gxLump.computeStrokesOnAllCorners(),
            [
                GXStroke.Stroke2,
                GXStroke.Stroke5,
                GXStroke.Stroke9,
                GXStroke.Stroke3,
            ],
        )

    def test_computeStrokesOnMainDiagonal(self):
        self.assertEqual(
            self.gxLump.computeStrokesOnMainDiagonal(),
            [
                GXStroke.Stroke2,
                GXStroke.Stroke3,
            ],
        )

    def test_computeStrokesOnAntiDiagonal(self):
        self.assertEqual(
            self.gxLump.computeStrokesOnAntiDiagonal(),
            [
                GXStroke.Stroke5,
                GXStroke.Stroke9,
            ],
        )

    def test_1(self):
        # 承（1/18590）
        gxLump = GXLump(util.constructCorners("1859"))
        self.assertEqual(gxLump.computeCode(), "1859")

        # 一（1/10000）
        gxLump = GXLump(util.constructCorners("1aaa"))
        self.assertEqual(gxLump.computeCode(), "1000")

        # 人（1/90000）
        gxLump = GXLump(util.constructCorners("9aaa"))
        self.assertEqual(gxLump.computeCode(), "9000")

    def test_2(self):
        # 于（1/70300）
        gxLump = GXLump(util.constructCorners("1a3c"))
        self.assertEqual(gxLump.computeCode(), "1030")

    def test_TopLeft_BottomRight(self):
        corners = (GXCorner.TopLeft, GXCorner.BottomRight)

        # 一（1/10000）
        gxLump = GXLump(util.constructCorners("1aaa"))
        self.assertEqual(gxLump.computeCode(corners), "10")

        # 人（1/90000）
        gxLump = GXLump(util.constructCorners("9aaa"))
        self.assertEqual(gxLump.computeCode(corners), "90")

    def test_TopRight_BottomLeft(self):
        corners = (GXCorner.TopRight, GXCorner.BottomLeft)

        # 一（1/10000）
        gxLump = GXLump(util.constructCorners("1aaa"))
        self.assertEqual(gxLump.computeCode(corners), "10")

        # 人（1/90000）
        gxLump = GXLump(util.constructCorners("9aaa"))
        self.assertEqual(gxLump.computeCode(corners), "90")
