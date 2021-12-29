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
		self.assertEqual(genVerticalPanes([1, 2, 3], LayoutFactory.DefaultBox),
				[Pane(8, 8, 247, 47.833333333333336), Pane(8, 47.833333333333336, 247, 127.5), Pane(8, 127.5, 247, 247)])
		self.assertEqual(genVerticalPanes([3, 2], LayoutFactory.DefaultBox),
				[Pane(8, 8, 247, 151.39999999999998), Pane(8, 151.39999999999998, 247, 246.99999999999997)])

	def test_genHorizontalPanes(self):
		self.assertEqual(genHorizontalPanes([1, 2, 3], LayoutFactory.DefaultBox),
				[Pane(8, 8, 47.833333333333336, 247), Pane(47.833333333333336, 8, 127.5, 247), Pane(127.5, 8, 247, 247)])
		self.assertEqual(genHorizontalPanes([3, 2], LayoutFactory.DefaultBox),
				[Pane(8, 8, 151.39999999999998, 247), Pane(151.39999999999998, 8, 246.99999999999997, 247)])

class LayoutGenerationTestCase(unittest.TestCase):
	def setUp(self):
		self.shapeFactory = LayoutFactory()

	def tearDown(self):
		pass

	def test_layout_Silkworm(self):
		layoutSpec = LayoutSpec(JointOperator.Silkworm, weights = [1, 2, 3])
		panes = self.shapeFactory.generateLayouts(layoutSpec)
		self.assertEqual(panes, [Pane(8, 8, 247, 47.833333333333336), Pane(8, 47.833333333333336, 247, 127.5), Pane(8, 127.5, 247, 247)])

		layoutSpec = LayoutSpec(JointOperator.Silkworm, weights = [3, 2])
		panes = self.shapeFactory.generateLayouts(layoutSpec)
		self.assertEqual(panes, [Pane(8, 8, 247, 151.39999999999998), Pane(8, 151.39999999999998, 247, 246.99999999999997)])

	def test_layout_Goose(self):
		layoutSpec = LayoutSpec(JointOperator.Goose, weights = [1, 2, 3])
		panes = self.shapeFactory.generateLayouts(layoutSpec)
		self.assertEqual(panes, [Pane(8, 8, 47.833333333333336, 247), Pane(47.833333333333336, 8, 127.5, 247), Pane(127.5, 8, 247, 247)])

		layoutSpec = LayoutSpec(JointOperator.Goose, weights = [3, 2])
		panes = self.shapeFactory.generateLayouts(layoutSpec)
		self.assertEqual(panes, [Pane(8, 8, 151.39999999999998, 247), Pane(151.39999999999998, 8, 246.99999999999997, 247)])

