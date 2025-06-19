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
        config,self.dungeon_list,message=json.load(open(f"{lang}_message.otrx",mode="r+"))
        self.prefix={};self.message={}
        self.prefix.update(config)
        self.message.update(message)

    def format_from_text(self, text, external: dict = None):
        pattern = re.compile(r'(?<!\\)\[([.\w]+)\]|(?<!\\)\{(\w+)\}')
        def repl(m):
            a, k = m.group(1), m.group(2)
            if a:
                if a.startswith('.'):
                    base = self
                    keys = a.lstrip('.').split('.')
                    return str(reduce(getattr, keys, base))
                else:
                    base = self.message
                    keys = a.split('.')
                    return str(reduce(operator.getitem, keys, base))
            return str((external or {})[k])
        out = text
        while True:
            nxt = pattern.sub(repl, out)
            if nxt == out:
                break
            out = nxt
        return re.sub(r'\\([\[\]\{\}])', r'\1', out)
    
    def format_from_id(self, id, external: dict = None):
        if id.startswith('.'):
            base, keys = self, id.lstrip('.').split('.')
            txt = reduce(getattr, keys, base)
        else:
            base, keys = self.message, id.split('.')
            i=0
            while i<len(keys):
                if keys[i].isdigit():
                    keys[i]=int(keys[i])
                i+=1
            txt = reduce(operator.getitem, keys, base)
        return self.format_from_text(str(txt), external)
    
lang=LanguageMessage("en")
dungeon_list=lang.dungeon_list
n,c,m,g = dungeon_list[random.choice(list(dungeon_list.keys()))]
hoge=True
print(lang.format_from_id("PATCH_TEXTS.map",{"dungeon_gender":g,"dungeon_name":n,"dungeon_state":f"[PATCH_TEXTS.{'masterful' if hoge else 'ordinary'}]"}))