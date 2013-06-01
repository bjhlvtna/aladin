# -*- coding: utf8 -*-
import os

def test():
    list = [{'key' : 1, 'value' : ['paul']},
            {'key' : 2, 'value' : ['bryan']},
            {'key' : 3, 'value' : ['sin']},
            {'key' : 2, 'value' : ['jin']},
            {'key' : 1, 'value' : ['edward']},
            {'key' : 1, 'value' : ['chris']}
            ]
    keyList = []
    newList = []

    for item in list :
        if item['key'] in keyList:
            idx = keyList.index(item['key'])
            newList[idx]['value'].append(item['value'][0])
        else:
            keyList.append(item['key'])
            newList.append(item)
    print newList

test()






