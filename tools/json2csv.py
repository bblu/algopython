# -*- coding: utf-8 -*-
import json

for line in open('son.json','r').readlines():
    obj = json.loads(line)
    print(obj.pageSize)
    for p in obj.rows:
        print(p)
