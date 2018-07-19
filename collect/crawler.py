import json
from datetime import datetime, timedelta

import requests

BASE_URL_FB_API = "https://graph.facebook.com/v3.0"
ACCESS_TOKEN = "EAAFkjXcYmBgBAPdTRO8UHLx0gB4178N0ZCN5196VuZA89KedSSYUc3p6bQMwPvopeJ0ch2W2dZCwiwhKbcpr8bvr9XLrVQjpZC9c5z6gLNZASFQ4FU9p3ReZAOXPXvowOCzd3b9HkYYaobllwRS9wpFZA9ZCic0YckHNDk4F5K7gZCmlPY2BloqXvKubzfyD87T9oADlb8PuXRwZDZD"
LIMIT_REQUEST = 20

#url 주면 json 데이터 return
def get_json_result(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        return "%s : Error for request [%s]" % (datetime.now(), url)


#페이스북 페이지 네임 주면 페이지 id값 return
def fb_name_to_id(pagename):

    base = BASE_URL_FB_API
    node = "/%s" % pagename
    params = "/?access_token=%s" % ACCESS_TOKEN
    url = base + node + params

    json_result = get_json_result()
    return json_result["id"]


#페이스북 페이지네임, 시작날짜, 끝날짜 주면 json->List형태로 데이터 return
def fb_get_post_list(pagename, from_date, to_date):
    page_id = fb_name_to_id(pagename)

    base = BASE_URL_FB_API
    node = "/%s/posts" %page_id
    fields = '/?fields=id,message,link,name,type,shares,'+\
            'created_time,comments.limit(0).summary(true),'+\
            'reactions.limit(0).summary(true)'
    duration = '&since=%s&until=%s' % (from_date, to_date)
    parameters = '&limit=%saccess_token=%s' % (LIMIT_REQUEST, ACCESS_TOKEN)
    url = base + node + fields + duration + parameters

    postList = []
    isNext = True
    while isNext:
        tmpPostList = get_json_result(url)
        for post in tmpPostList["data"]:
            postVo = preprocess_post(post)
            postList.append(postVo)

        paging = tmpPostList.get("paging").get("next")
        if paging != None:
            url = paging
        else:
            isNext = False

    #결과를 파일로 저장
    with open("C:/Users/aran0/Desktop/BIT/python/facebook/" + pagename + ".json", 'w', encoding = 'utf-8') as outfile:
        json_string = json.dumps(postList, indent = 4, sort_keys = True, ensure_ascii = False)
        outfile.write(json_string)

    return postList

def preprocess_post(post):

    #작성일(+9시간 해주기)
    created_time = post["created_time"]
    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
    created_time = created_time + timedelta(hours=+9)
    created_time = created_time.strftime('%Y-%m-%d%H:%M:%S')

    #공유 수
    if "shares" not in post :
        shares_count = 0
    else :
        shares_count = post["shares"]["count"]


    #리액션 수
    if "reactions" not in post:
        reactions_count = 0
    else:
        reactions_count = post["reactions"]["summary"]["total_count"]


    #댓글 수
    if "comments" not in post:
        comments_count = 0
    else:
        comments_count = post["comments"]["summary"]["total_count"]


    #메시지 수
    if "message" not in post:
        message_str = ""
    else:
        message_str = post["message"]

    postVo = {
                "created_time" : created_time,
                "shares_count" : shares_count,
                "reactions_count" : reactions_count,
                "comments_count" : comments_count,
                "message_str" : message_str
            }

    return postVo

