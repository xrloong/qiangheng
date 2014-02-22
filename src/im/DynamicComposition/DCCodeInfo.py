from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane
from .Calligraphy import StrokeGroup

class DCCodeInfo(CodeInfo):
	PANE_NAME_DEFAULT="瑲珩預設範圍名稱"
	PANE_NAME_QI="起"
	PANE_NAME_LIAO="廖"
	PANE_NAME_DAO="斗"
	PANE_NAME_ZAI="載"

	PANE_NAME_MU_1="畞:1"
	PANE_NAME_MU_2="畞:2"

	PANE_NAME_YOU_1="幽:1"
	PANE_NAME_YOU_2="幽:2"

	PANE_NAME_LIANG_1="㒳:1"
	PANE_NAME_LIANG_2="㒳:2"

	PANE_NAME_JIA_1="夾:1"
	PANE_NAME_JIA_2="夾:2"

	PANE_NAME_ZUO_1="㘴:1"
	PANE_NAME_ZUO_2="㘴:2"

	def __init__(self, strokeGroup):
		CodeInfo.__init__(self)

		self.strokeGroup=strokeGroup
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : Pane.DEFAULT_PANE}

	@staticmethod
	def generateDefaultCodeInfo(strokeGroup):
		codeInfo=DCCodeInfo(strokeGroup)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeGroup.getStrokeList()

	def getCode(self):
		strokeList=self.getStrokeList()
		codeList=[stroke.getCode() for stroke in strokeList]
		return ','.join(codeList)

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=Pane.DEFAULT_PANE

	def setExtraPane(self, extraPane, paneName):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)

	def getStrokeGroup(self):
		return self.strokeGroup

	def transform(self, pane):
		self.strokeGroup.transform(pane)

