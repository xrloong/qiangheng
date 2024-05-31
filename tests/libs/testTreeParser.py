import unittest

from tree.node import Node
from tree.parser import TreeParser

class TreeParserTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testParseSimpleNode(self):
		nodeAnswer = Node()

		node = TreeParser.parse("()")
		self.assertEqual(node, nodeAnswer)

	def testParseLeafProp(self):
		nodeAnswer = Node(prop = {"測試屬性": "測試值"})

		node = TreeParser.parse("({測試屬性=測試值})")
		self.assertEqual(node, nodeAnswer)

	def testParseChildren(self):
		node1 = Node(prop = {"測試屬性": "測試值"})
		node2 = Node()
		nodeAnswer = Node(prop = {"測試運算": "測試"}, children =(node1, node2))

		node = TreeParser.parse("({測試運算=測試} ({測試屬性=測試值}) ())")
		self.assertEqual(node, nodeAnswer)

	def testParseLeafNode(self):
		nodeAnswer = Node(prop = {"置換": "倉"})

		node = TreeParser.parse("({置換=倉})")
		self.assertEqual(node, nodeAnswer)

	def testParseCompositionNode(self):
		node王 = Node(prop = {"置換": "王"})
		node倉 = Node(prop = {"置換": "倉"})
		nodeAnswer = Node(prop = {"運算": "鴻"}, children =(node王, node倉))

		node = TreeParser.parse("({運算=鴻} ({置換=王}) ({置換=倉}))")
		self.assertEqual(node, nodeAnswer)

