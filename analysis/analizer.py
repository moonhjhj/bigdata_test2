import json
import re

from konlpy.tag import Twitter
from collections import Counter


#json파일명, 추출 데이터 key값 주면 문자열 return

def json_to_str(filename, key):
    jsonfile = open(filename, 'r', encoding = 'utf-8')
    json_string = jsonfile.read()
    jsondata = json.loads(json_string)


    data = ''

    for item in jsondata:
        value = item.get(key)
        if value is None:
            continue
        data += re.sub(r'[^\w]', '', value)


    return data


#명사를 추출해서 빈도수 알려줌
def count_wordfreq(data):
    twitter = Twitter()
    nouns = twitter.nouns(data)

    count = Counter(nouns)
    return count