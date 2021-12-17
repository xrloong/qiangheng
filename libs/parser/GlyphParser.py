import ruamel.yaml as yaml
import abc

from collections import OrderedDict

class GlyphElementDescription:
	def __init__(self, method):
		self.method = method

		self.name = None
		self.referenceName = None
		self.order = None

		self.strokeType = None
		self.startPoint = None
		self.params = None

		self.position = None

	@property
	def isAnchor(self):
		return self.method == GlyphTags.METHOD__ANCHOR

	@property
	def isReference(self):
		return self.method == GlyphTags.METHOD__REFERENCE

	@property
	def isDefinition(self):
		return self.method == GlyphTags.METHOD__DEFINITION

class GlyphComponentDescription:
	def __init__(self, name, comment = None):
		self.name = name
		self.comment = comment
		self.elements = None

class GlyphDataSetDescription:
	def __init__(self, components: [GlyphComponentDescription]):
		self.components = components

class GlyphTags(object):
	TEMPLATE_SET = "樣式集"
	STROKE_GROUP='筆劃組'
	STROKE='筆劃'
	NAME='名稱'
	COMMENT='註記'

	METHOD='方式'
	TYPE='類型'
	START_POINT='起始點'
	PARAMETER='參數'

	METHOD__DEFINITION='定義'
	METHOD__REFERENCE='引用'
	METHOD__ANCHOR='錨點'

	REFRENCE_NAME='引用名稱'
	ORDER='順序'

	POSITION='定位'

class GlyphParser(object):
	def __init__(self):
		super().__init__()

	def load(self, filename):
		rootNode = yaml.load(open(filename), Loader=yaml.SafeLoader)
		dataSet = self.parseDataSet(rootNode)
		return dataSet

	def parseElement(self, elementNode):
		method = elementNode.get(GlyphTags.METHOD)
		element = GlyphElementDescription(method)
		elementDict = OrderedDict({GlyphTags.METHOD: method})
		if element.isReference:
			referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
			order = elementNode.get(GlyphTags.ORDER)
			position = elementNode.get(GlyphTags.POSITION)

			element.referenceName = referenceName
			element.order = order
			if position:
				element.position = position
		elif element.isAnchor:
			name = elementNode.get(GlyphTags.NAME)
			referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
			position = elementNode.get(GlyphTags.POSITION)

			element.name = name
			element.referenceName = referenceName
			if position:
				element.position = position
		elif element.isDefinition:
			strokeType = elementNode.get(GlyphTags.TYPE)
			startPoint = elementNode.get(GlyphTags.START_POINT)
			params = elementNode.get(GlyphTags.PARAMETER)
			position = elementNode.get(GlyphTags.POSITION)

			element.strokeType = strokeType
			element.startPoint = startPoint
			element.params = params
			element.position = position
		return element

	def parseComponent(self, componentNode):
		componentName = componentNode.get(GlyphTags.NAME)
		componentComment = componentNode.get(GlyphTags.COMMENT)
		strokeGroupNode = componentNode.get(GlyphTags.STROKE_GROUP)

		component = GlyphComponentDescription(componentName, componentComment)

		elements = []
		for elementNode in strokeGroupNode.get(GlyphTags.STROKE):
			element = self.parseElement(elementNode)
			elements.append(element)

		component.elements = elements
		return component

	def parseDataSet(self, rootNode):
		dataSetNode=rootNode.get(GlyphTags.TEMPLATE_SET)

		components = []
		for componentNode in dataSetNode:
			component = self.parseComponent(componentNode)
			components.append(component)

		dataSet = GlyphDataSetDescription(components)
		return dataSet

class IfGlyphDescriptionInterpreter(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def interpretElement(self, element: GlyphElementDescription):
		pass

	@abc.abstractmethod
	def interpretComponent(self, component: GlyphComponentDescription):
		pass

	@abc.abstractmethod
	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		pass

