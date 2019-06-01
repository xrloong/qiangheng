
class FCLump:
	def __init__(self, corners):
		_top_left, _top_right, _bottom_left, _bottom_right = corners
		self._top_left = _top_left
		self._top_right = _top_right
		self._bottom_left = _bottom_left
		self._bottom_right = _bottom_right

	@property
	def topLeft(self):
		return self._top_left

	@property
	def topRight(self):
		return self._top_right

	@property
	def bottomLeft(self):
		return self._bottom_left

	@property
	def bottomRight(self):
		return self._bottom_right

