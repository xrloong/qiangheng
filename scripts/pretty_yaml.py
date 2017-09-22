import yaml
import yaml.dumper
import sys
from collections import OrderedDict

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

class quoted_str(str): pass
def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

class flowseq(list): pass
def flowseq_rep(dumper, data):
    return dumper.represent_sequence( u'tag:yaml.org,2002:seq', data, flow_style=True)

class flowmap(OrderedDict): pass
def flowmap_rep(dumper, data):
    return dumper.represent_mapping( u'tag:yaml.org,2002:map', data.items(), flow_style=True)
represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
yaml.add_representer(OrderedDict, represent_dict_order)  
#yaml.add_representer(str, quoted_presenter)
yaml.add_representer(quoted_str, quoted_presenter)
yaml.add_representer(flowseq, flowseq_rep)
yaml.add_representer(flowmap, flowmap_rep)

infile = sys.argv[1]
outfile = sys.argv[2]
node=ordered_load(open(infile, "r"), yaml.CLoader)



def adjust(n):
	if isinstance(n, dict):
		for x in n.items():
			key, value = x
			if isinstance(value, str):
				n[key]=quoted_str(value)
			else:
				adjust(value)
		"""
		if '起始點' in n:
			n['起始點'] = flowseq(n['起始點'])
		if '參數' in n:
			n['參數'] = flowseq(n['參數'])
		if '順序' in n:
			n['順序'] = flowseq(n['順序'])
		if '定位' in n:
			n['定位'] = flowseq(n['定位'])
		"""
		if '筆劃' in n:
			n['筆劃'] = [flowmap(s) for s in n['筆劃']]
	elif isinstance(n, list) or isinstance(n, tuple):
		for x in n:
			adjust(x)

adjust(node)
yaml.dump(node, open(outfile, "w"), Dumper=MyDumper,
	allow_unicode=True, default_flow_style=False,
	explicit_start=True, explicit_end=True)


