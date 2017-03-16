from model.base.CodeInfo import CodeInfo
from xie.graphics.shape import Pane
from xie.graphics.stroke import StrokeGroup
from xie.graphics.stroke import StrokeGroupInfo

class DCStrokeGroup:
	def __init__(self, strokeGroup):
		self.strokeGroup=strokeGroup
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : Pane.EMBOX}

	def getCount(self):
		return self.strokeGroup.getCount()

	def getStrokeGroup(self):
		return self.strokeGroup

	def getStrokeList(self):
		return self.strokeGroup.getStrokeList()

	def generateStrokeGroup(self, pane):
		return StrokeGroup.generateStrokeGroup(self.strokeGroup, pane)

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=Pane.EMBOX

	def setExtraPane(self, paneName, extraPane):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)

	@staticmethod
	def generateDefaultStrokeGroup(dcStrokeGroupPanePair):
		strokeGroupPanePair=[(pair[0].getStrokeGroup(), pair[1]) for pair in dcStrokeGroupPanePair]
		strokeGroupInfo=StrokeGroup.generateStrokeGroupInfo(strokeGroupPanePair)
		strokeGroup=StrokeGroup(strokeGroupInfo)
		strokeGroup=DCStrokeGroup(strokeGroup)
		return strokeGroup

	@staticmethod
	def generateStrokeGroupByParameter(strokeList):
		strokeGroupInfo=StrokeGroupInfo.generateInstanceByStrokeList(strokeList)
		strokeGroup=StrokeGroup(strokeGroupInfo)
		return DCStrokeGroup(strokeGroup)

class DCCodeInfo(CodeInfo):
	PANE_NAME_DEFAULT="瑲珩預設範圍名稱"

	PANE_NAME_LOOP="回"
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

	STROKE_GROUP_NAME_DEFAULT="瑲珩預設筆劃組名稱"

	STROKE_GROUP_NAME_LOOP="回"
	STROKE_GROUP_NAME_QI="起"
	STROKE_GROUP_NAME_LIAO="廖"
	STROKE_GROUP_NAME_DAO="斗"
	STROKE_GROUP_NAME_ZAI="載"

	STROKE_GROUP_NAME_MU="畞"
	STROKE_GROUP_NAME_YOU="幽"
	STROKE_GROUP_NAME_LIANG="㒳"
	STROKE_GROUP_NAME_JIA="夾"
	STROKE_GROUP_NAME_ZUO="㘴"

	def __init__(self, strokeGroupDB):
		super().__init__()

		self.strokeGroupDB=strokeGroupDB

	@staticmethod
	def generateDefaultCodeInfo(strokeGroupPanePair):
		strokeGroup=DCStrokeGroup.generateDefaultStrokeGroup(strokeGroupPanePair)
		strokeGroupDB={DCCodeInfo.STROKE_GROUP_NAME_DEFAULT : strokeGroup}

		codeInfo=DCCodeInfo(strokeGroupDB)
		return codeInfo

	def toCode(self):
		strokeList=self.getStrokeGroup().getStrokeList()
		return strokeList

	def setExtraPane(self, strokeGroupName, paneName, extraPane):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		strokeGroup.setExtraPane(paneName, extraPane)

	def getExtraPane(self, strokeGroupName, paneName):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		return strokeGroup.getExtraPane(paneName)

	def getStrokeGroup(self, strokeGroupName=STROKE_GROUP_NAME_DEFAULT):
		strokeGroup=self.strokeGroupDB.get(strokeGroupName)
		if strokeGroupName!=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT and strokeGroup==None:
			strokeGroup=self.getStrokeGroup(DCCodeInfo.STROKE_GROUP_NAME_DEFAULT)
		return strokeGroup

	def getStrokeCount(self):
		return self.getStrokeGroup().getCount()

