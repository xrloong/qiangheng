"""輸出編碼表的快速 YAML 序列化。

針對編碼表的資料形狀（巢狀 dict/list、葉值皆為 str、block 風格、鍵排序）
直接產生文字，輸出與下列設定的 ruamel 純 Python dumper 逐位元組相同：

    YAML(typ="safe")、explicit_start/end、allow_unicode、
    default_flow_style=False、width 預設（80）

任何超出這個安全範圍的資料（非 str 葉值、空容器、含空白或需要
plain/single-quote 以外風格的字串、序列中的長字串……）一律拋出
FallbackNeeded，由呼叫端改用 ruamel 輸出整份文件。風格判定本身
委派給 ruamel 的 analyze_scalar 與 resolver，並以字串為鍵快取。
"""

import io

from ruamel.yaml.emitter import Emitter
from ruamel.yaml.nodes import ScalarNode
from ruamel.yaml.resolver import Resolver

WIDTH = 80
STR_TAG = "tag:yaml.org,2002:str"

PLAIN = 1
SINGLE_QUOTED = 2


class FallbackNeeded(Exception):
    pass


class _ScalarStyler:
    def __init__(self):
        self.__emitter = Emitter(io.StringIO(), allow_unicode=True)
        self.__resolver = Resolver()
        self.__cache = {}

    def styleOf(self, s: str):
        style = self.__cache.get(s)
        if style is None:
            style = self.__computeStyle(s)
            self.__cache[s] = style
        return style

    def __computeStyle(self, s: str):
        if not s or "\n" in s or " " in s:
            raise FallbackNeeded(s)
        analysis = self.__emitter.analyze_scalar(s)
        resolvedTag = self.__resolver.resolve(ScalarNode, s, (True, False))
        if str(resolvedTag) == STR_TAG and analysis.allow_block_plain:
            return PLAIN
        if analysis.allow_single_quoted and "'" not in s:
            return SINGLE_QUOTED
        raise FallbackNeeded(s)


class FastYamlDumper:
    def __init__(self):
        self.__styler = _ScalarStyler()

    def dumps(self, data: dict) -> str:
        if not isinstance(data, dict) or not data:
            raise FallbackNeeded(data)
        fragments = ["---\n"]
        self.__renderMap(data, 0, fragments, inlineFirst=False)
        fragments.append("...\n")
        return "".join(fragments)

    def __valueText(self, s):
        style = self.__styler.styleOf(s)
        if style == PLAIN:
            return s
        return "'" + s + "'"

    def __keyText(self, s):
        if self.__styler.styleOf(s) != PLAIN:
            raise FallbackNeeded(s)
        return s

    def __renderMap(self, node, indent, fragments, inlineFirst):
        pad = " " * indent
        first = True
        for key, value in sorted(node.items()):
            if not isinstance(key, str):
                raise FallbackNeeded(key)
            keyText = self.__keyText(key)
            lead = "" if (first and inlineFirst) else pad
            first = False
            if isinstance(value, str):
                style = self.__styler.styleOf(value)
                valueText = value if style == PLAIN else "'" + value + "'"
                column = indent + len(keyText) + 2
                # 只有 plain 風格在超寬時折行；無空白的單引號字串不折行
                if style == PLAIN and column + len(valueText) > WIDTH:
                    fragments.append(
                        lead + keyText + ": \n" + " " * (indent + 2) + valueText + "\n"
                    )
                else:
                    fragments.append(lead + keyText + ": " + valueText + "\n")
            elif isinstance(value, dict):
                if not value:
                    raise FallbackNeeded(value)
                fragments.append(lead + keyText + ":\n")
                self.__renderMap(value, indent + 2, fragments, inlineFirst=False)
            elif isinstance(value, list):
                if not value:
                    raise FallbackNeeded(value)
                fragments.append(lead + keyText + ":\n")
                self.__renderSeq(value, indent, fragments)
            else:
                raise FallbackNeeded(value)

    def __renderSeq(self, node, indent, fragments):
        pad = " " * indent
        for item in node:
            if isinstance(item, dict):
                if not item:
                    raise FallbackNeeded(item)
                fragments.append(pad + "- ")
                self.__renderMap(item, indent + 2, fragments, inlineFirst=True)
            elif isinstance(item, str):
                itemText = self.__valueText(item)
                if indent + 2 + len(itemText) > WIDTH:
                    raise FallbackNeeded(item)
                fragments.append(pad + "- " + itemText + "\n")
            else:
                raise FallbackNeeded(item)
