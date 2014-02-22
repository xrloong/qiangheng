
import char
import im

filename='U4E00-U9FA6.txt'
fileencoding='utf-8'
f=open(filename, encoding=fileencoding)

def checkgrammar(g):
	if g[0]=='(' and g[-1]==')':
		if len(g)==3 and g[1]=='龜':
			return True
		elif len(g)==5 and g[1] in ['林', '爻', '卅', '鑫', '燚']:
#			['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
			return True
		elif len(g)==6 and g[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾',]:
#			['好', '志',
#			'回', '同', '函', '區', '左',
#			'起', '廖', '載', '聖', '句',
#			'夾', '衍', '衷',]
			return True
		elif len(g)==7 and g[1] in ['算', '湘', '霜', '想', '怡', '穎',]:
			return True
		elif len(g)==8 and g[1] in ['纂',]:
#			['纂', '膷',]
			return True
		else:
			return False
	else:
		return False
	return True

chlist=[]
chdict={}
for line in f.readlines():
	l=line.strip()
	if not l: continue
	elif l[0]=='#': continue
	ll=l.split('\t')
	if len(ll)>=3:
		if not checkgrammar(ll[2]):
			print("錯誤的表達式 %s=%s"%(ll[1], ll[2]))
		else:
			chlist.append(ll[1])
			chdict[ll[1]]=char.Char(ll[1], ll[2:])

imchoices=['倉', '行', '易', '無', '鄭']
choice=imchoices[1]

codelist=[]
if choice=='倉':
	print(chdict['王'].cj)
	im.CangJie()
elif choice=='行':
	print(chdict['王'].ar)
	im.Array()
elif choice=='易':
	print(chdict['王'].dy)
	im.DaYi()
elif choice=='無':
	print(chdict['王'].bs)
	im.Boshiamy()
elif choice=='鄭':
	print(chdict['王'].zm)
	im.ZhengMa()

