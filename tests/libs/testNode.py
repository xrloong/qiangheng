import unittest

from tree.node import Node
from tree.parser import TreeParser

class TreeParserTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testDefault(self):
		node = Node()

		self.assertEqual(node.prop, {})
		self.assertEqual(node.children, ())

	def testProp(self):
		node = Node(prop = {"測試屬性": "測試值"})
		self.assertEqual(node.prop, {"測試屬性": "測試值"})

	def testChildren(self):
		node1 = Node(prop = {"測試屬性": "測試值"})
		node2 = Node(prop = {"置換": "倉"})
		node = Node(children = (node1, node2))

		self.assertEqual(node.children, (node1, node2))

	def test_倉(self):
		node倉 = Node(prop = {"置換": "倉"})
		self.assertEqual(node倉.prop, {"置換": "倉"})

	def test_瑲(self):
		node王 = Node(prop = {"置換": "王"})
		node倉 = Node(prop = {"置換": "倉"})
		node瑲 = Node(prop = {"運算": "鴻"}, children = (node王, node倉))

		self.assertEqual(node瑲.prop, {"運算": "鴻"})
		self.assertEqual(node瑲.children, (node王, node倉))

