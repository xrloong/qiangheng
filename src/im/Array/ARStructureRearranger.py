from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class ARStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		lenCompList=len(compList)

		if operator.getName()=='鴻' and lenCompList>=2:
			firstChilStructDesc=compList[0]
			secondChilStructDesc=compList[1]

			firstName=firstChilStructDesc.getReferenceName()
			secondName=secondChilStructDesc.getReferenceName()

			secondeCompList=secondChilStructDesc.getCompList()
			if firstName=='彳' and len(secondeCompList)>=2:
				secondFirstChilStructDesc=secondeCompList[0]
				secondSecondChilStructDesc=secondeCompList[1]

				secondFirstName=secondFirstChilStructDesc.getReferenceName()
				secondSecondName=secondSecondChilStructDesc.getReferenceName()

				isMatch=(secondFirstName=='山' and secondSecondName=='一')

				if isMatch:
					newStructDesc=self.generateStructureDescriptionWithName('[特微]')
					structDescList=[newStructDesc]+secondeCompList[2:]+compList[2:]
					structDesc.setCompList(structDescList)
					structDesc.setOperator(Operator.OperatorGoose)
			if secondName=='[䘗中]':
				newStructDesc=self.generateStructureDescriptionWithName('[特微]')
				newStructDesc_糸=self.generateStructureDescriptionWithName('糸')
				structDescList=[newStructDesc, newStructDesc_糸]+compList[2:]
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorGoose)

		if operator.getName()=='蚕' and lenCompList>=2:
			self.rearrangeForSilkworm(structDesc)

		if operator.getName() in ['範載', '範同'] and lenCompList>=2:
			self.rearrangeForZai(structDesc)

		if operator.getName()=='範湘' and lenCompList>=2:
			self.rearrangeForFanYan(structDesc)

	def getRearrangeListZai(self):
		rearrangeList=[
			['戈', '口', ['[一口]', '[特戈]']],
			['戈', '[口一]', ['[一口]', '一', '[特戈]']],
			['戈', '呈', ['[一口]', '王', '[特戈]']],
			['戈', '[口天]', ['[一口]', '天', '[特戈]']],
			['戈', '[特㦽]', ['[一口]', '[一巛]', '[特戈]']],

			['戌', '口', ['厂', '[一口]', '[特戈]']],
			]
		return rearrangeList

	def getRearrangeListSilkworm(self):
		rearrangeList=[
			['一', '[壴下]', ['[一口]']],
			['一', '口', ['[一口]']],
			['旦', '黾', ['日', '[一口]', '电']],
			['一', '[口㐄]', ['[一口]', '㐄']],
			['士', '冖', ['[士冖]']],
			['文', '厂', ['[文厂]']],
			]
		return rearrangeList

	def getRearrangeListFanYan(self):
		rearrangeList=[
			['儿.0', '儿.1', ['丨', '乚']],
			['[丨丨].0', '[丨丨].1', ['丨', '丨']],
			['[丨丿].0', '[丨丿].1', ['丨', '丿']],
			['[丿丨].0', '[丿丨].1', ['丨', '丨']],
			]
		return rearrangeList

