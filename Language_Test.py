"""
text rule:
[] >> replace using internal dict phrase
{} >> replace using external phrase
"""

import json,re
import operator
from functools import reduce
import random

class LanguageMessage:
    def __init__(self,lang):
        message=json.load(open(f"{lang}_message.otrx",mode="r+"))
        self.__dict__.update(message)

    def _dict_get(self, obj, key):
        if isinstance(obj, (list, tuple)):
            return obj[int(key, 0)]
        return obj[key]

    def format_from_text(self, text, external: dict = None):
        pattern = re.compile(r'(?<!\\)\[([.\w]+)\]|(?<!\\)\{(\w+)\}')
        def repl(m):
            a, k = m.group(1), m.group(2)
            if a:
                keys = a.split('.')
                key = keys.pop(0) if len(keys)>1 else keys
                i=0
                while i<len(keys):
                    if keys[i].isdigit():
                        keys[i]=int(keys[i])
                    i+=1
                base = getattr(self,key)
                return str(reduce(self._dict_get,keys,base))
            return str((external or {})[k])
        out = text
        while True:
            nxt = pattern.sub(repl, out)
            if nxt == out:
                break
            out = nxt
        return re.sub(r'\\([\[\]\{\}])', r'\1', out)
    
    def format_from_id(self, id, external: dict = None):
        keys = id.split('.')
        if len(keys)>1:
            key=keys.pop(0)
        else: key=keys
        base = getattr(self,key)
        i=0
        while i<len(keys):
            if keys[i].isdigit():
                keys[i]=int(keys[i])
            i+=1
        txt = reduce(self._dict_get,keys,base)
        return self.format_from_text(str(txt), external)
    
lang=LanguageMessage("en")
dungeon_list=lang.dungeon_list
n,c,m,g = dungeon_list[random.choice(list(dungeon_list.keys()))]
hoge=True
print(lang.format_from_id("PATCH_TEXTS.map",{"dungeon_gender":g,"dungeon_name":n,"dungeon_state":f"[PATCH_TEXTS.{'masterful' if hoge else 'ordinary'}]"}))