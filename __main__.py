from collect import crawler
from analysis import analizer
from visualize import visualizer

pagename = "channelanews"
from_date = "2018-05-30"
to_date = "2018-05-31"

if __name__ == "__main__" :

    #수집
    postList = crawler.fb_get_post_list(pagename, from_date, to_date)
    print(postList)

    #분석
    dataString = analizer.json_to_str("C:/Users/aran0/Desktop/BIT/python/facebook/channelanews.json", "message_str")
    count_data = analizer.count_wordfreq(dataString)
    print(count_data)

    dictWord = dict(count_data.most_common(20))

    #그래프
    visualizer.show_graph_bar(dictWord, pagename)
    visualizer.wordcloud(dictWord, pagename)