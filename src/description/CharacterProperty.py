
class CharacterProperty:
	def __init__(self):
		self.prop={}
		self.updateProperty({})

	def getProperty(self):
		return self.prop

	def updateProperty(self, prop):
		self.prop.update(prop)
		self.freq=self.prop.get('頻率', 0)
		self.note=self.prop.get('註記', "")

	def getFrequency(self):
		return self.freq

