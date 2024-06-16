import unittest

from xie.graphics.shape import Pane

from coding.DynamicComposition.layout import JointOperator
from coding.DynamicComposition.layout import LayoutSpec
from coding.DynamicComposition.layout import LayoutFactory
from coding.DynamicComposition.layout import genVerticalPanes, genHorizontalPanes


class PaneUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_genVerticalPanes(self):
        self.assertEqual(
            genVerticalPanes([1, 2, 3], LayoutFactory.DefaultBox),
            [
                (8, 8, 247, 47.833333333333336),
                (8, 47.833333333333336, 247, 127.5),
                (8, 127.5, 247, 247),
            ],
        )
        self.assertEqual(
            genVerticalPanes([3, 2], LayoutFactory.DefaultBox),
            [
                (8, 8, 247, 151.39999999999998),
                (8, 151.39999999999998, 247, 246.99999999999997),
            ],
        )

    def test_genHorizontalPanes(self):
        self.assertEqual(
            genHorizontalPanes([1, 2, 3], LayoutFactory.DefaultBox),
            [
                (8, 8, 47.833333333333336, 247),
                (47.833333333333336, 8, 127.5, 247),
                (127.5, 8, 247, 247),
            ],
        )
        self.assertEqual(
            genHorizontalPanes([3, 2], LayoutFactory.DefaultBox),
            [
                (8, 8, 151.39999999999998, 247),
                (151.39999999999998, 8, 246.99999999999997, 247),
            ],
        )


class LayoutGenerationTestCase(unittest.TestCase):
    def setUp(self):
        self.shapeFactory = LayoutFactory()

    def tearDown(self):
        pass

    def test_layout_Silkworm(self):
        layoutSpec = LayoutSpec(JointOperator.Silkworm, weights=[1, 2, 3])
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 47.833333333333336),
                Pane(8, 47.833333333333336, 247, 127.5),
                Pane(8, 127.5, 247, 247),
            ],
        )

        layoutSpec = LayoutSpec(JointOperator.Silkworm, weights=[3, 2])
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 151.39999999999998),
                Pane(8, 151.39999999999998, 247, 246.99999999999997),
            ],
        )

    def test_layout_Goose(self):
        layoutSpec = LayoutSpec(JointOperator.Goose, weights=[1, 2, 3])
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 47.833333333333336, 247),
                Pane(47.833333333333336, 8, 127.5, 247),
                Pane(127.5, 8, 247, 247),
            ],
        )

        layoutSpec = LayoutSpec(JointOperator.Goose, weights=[3, 2])
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 151.39999999999998, 247),
                Pane(151.39999999999998, 8, 246.99999999999997, 247),
            ],
        )

    def test_layout_Loop(self):
        layoutSpec = LayoutSpec(JointOperator.Loop)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [Pane(8, 8, 247, 247), Pane(87.666667, 87.666667, 167.333333, 167.333333)],
        )

    def test_layout_Qi(self):
        layoutSpec = LayoutSpec(JointOperator.Qi)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(panes, [Pane(8, 8, 247, 247), Pane(127.5, 8, 247, 127.5)])

    def test_layout_Liao(self):
        layoutSpec = LayoutSpec(JointOperator.Liao)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(panes, [Pane(8, 8, 247, 247), Pane(127.5, 127.5, 247, 247)])

    def test_layout_Zai(self):
        layoutSpec = LayoutSpec(JointOperator.Zai)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(panes, [Pane(8, 8, 247, 247), Pane(8, 127.5, 127.5, 247)])

    def test_layout_Dou(self):
        layoutSpec = LayoutSpec(JointOperator.Dou)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(panes, [Pane(8, 8, 247, 247), Pane(8, 8, 127.5, 127.5)])

    def test_layout_Mu(self):
        layoutSpec = LayoutSpec(JointOperator.Mu)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 247),
                Pane(8, 127.5, 127.5, 247),
                Pane(127.5, 127.5, 247, 247),
            ],
        )

    def test_layout_Zuo(self):
        layoutSpec = LayoutSpec(JointOperator.Zuo)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 247),
                Pane(8, 8, 127.5, 127.5),
                Pane(127.5, 8, 247, 127.5),
            ],
        )

    def test_layout_You(self):
        layoutSpec = LayoutSpec(JointOperator.You)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 247),
                Pane(31.9, 8, 103.6, 199.2),
                Pane(151.4, 8, 223.1, 199.2),
            ],
        )

    def test_layout_Liang(self):
        layoutSpec = LayoutSpec(JointOperator.Liang)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 247),
                Pane(31.9, 55.8, 103.6, 247),
                Pane(151.4, 55.8, 223.1, 247),
            ],
        )

    def test_layout_Jia(self):
        layoutSpec = LayoutSpec(JointOperator.Jia)
        panes = self.shapeFactory.generateLayouts(layoutSpec)
        self.assertEqual(
            panes,
            [
                Pane(8, 8, 247, 247),
                Pane(8, 55.8, 103.6, 199.2),
                Pane(151.4, 55.8, 247, 199.2),
            ],
        )
