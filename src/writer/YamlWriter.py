import yaml

class YamlWriter:
	def write(self, imInfo, codeMappingInfoList):
		rootNode="輸入法"
		nameNode={"輸入法名稱": {
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
				"SG":imInfo.getName('sg'),
				}}

                # 按鍵與顯示的對照表
		l=[]
		keyMaps=imInfo.getKeyMaps()
		for key, disp in keyMaps:
			attrib={"按鍵對應": {"按鍵":key, "顯示":disp} }
			l.append(attrib)
		keyMappingSet={"按鍵對應集":l}

		l=[]
		for x in sorted(codeMappingInfoList, key=lambda y: y.getKey()):
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "頻率":x.getFrequency(), "類型":x.getVariance()}
			l.append(attrib)
		codeMappingSet={"對應集":l}

		l=[nameNode, keyMappingSet, codeMappingSet]
		print(yaml.dump(l, allow_unicode=True))

