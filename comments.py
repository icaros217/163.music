# -*- coding: utf-8 -*-
"""
根据歌曲 ID 获得所有的歌曲所对应的评论信息
"""
import re
import requests
import sql
import time
import threading
import pymysql.cursors
import sys,os
reload(sys)
sys.setdefaultencoding('utf8')

class Comments(object):
    headers = {
        'Host': 'music.163.com',
        'Connection': 'keep-alive',
        'Content-Length': '484',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cookie': 'JSESSIONID-WYYY=b66d89ed74ae9e94ead89b16e475556e763dd34f95e6ca357d06830a210abc7b685e82318b9d1d5b52ac4f4b9a55024c7a34024fddaee852404ed410933db994dcc0e398f61e670bfeea81105cbe098294e39ac566e1d5aa7232df741870ba1fe96e5cede8372ca587275d35c1a5d1b23a11e274a4c249afba03e20fa2dafb7a16eebdf6%3A1476373826753; _iuqxldmzr_=25; _ntes_nnid=7fa73e96706f26f3ada99abba6c4a6b2,1476372027128; _ntes_nuid=7fa73e96706f26f3ada99abba6c4a6b2; __utma=94650624.748605760.1476372027.1476372027.1476372027.1; __utmb=94650624.4.10.1476372027; __utmc=94650624; __utmz=94650624.1476372027.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    params = {
        'csrf_token': 'fc283388ca7e30d0f4b3a844fa68a12f'
    }

    data = {
        'params': 'j9r9EAB6yiF5L6k2ctg5hs67ZrCuh6398852WA3cBccPAA2wNdpbVqJbxU+e7N0nDg6CSioTsfU7xveieeOfDqogCUpnPkHZ42BjK9p47u2U49FUuwSnvOcRD0ZTxB/ypxfOGZVUkCZnnsb2VERggF3tHWh+3v5vDDciLg4EiGLQz3WvCgu1mEQN/fhd45rFIxj3SxGljA4+l5skjItrjIEL6N1kf6Lsn2cFb076Ir0=',
        'encSecKey': 'cec377944368a80dfda604696caa7b6a6f03889c51c8e4086414b4307347dec5b0f38b7519a228b343affe105fbf8c2eb8a9dfb1ce3ee8248ec47d1bedccea2c5794777932628112ceb65d138bffab68a682c66fdcaee44f478406fe417e9c640584289a943f3809ad924377c7dd2ac08085219435a393a48cbde7823cab0273'
    }

   # proxies = { "http": "http://123.59.10.44:80",
     #            "https": "http://115.194.41.174:8118",}

    def get_comments(self, music_id, flag):
        self.headers['Referer'] = 'http://music.163.com/playlist?id=' + str(music_id)
        if flag:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data)
        else:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data)
        return r.json()


if __name__ == '__main__':
    my_comment = Comments()
    highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    def save_comments(musics, flag, connection0):
        for i in musics:
            my_music_id = i['MUSIC_ID']
            my_music_name = i['MUSIC_NAME']
            my_artist_name = i['ARTIST_NAME']
            try:
                comments = my_comment.get_comments(my_music_id, flag)
                hotcomments = comments['hotComments']


                if comments['total'] > 10000:

                    results = ''
                    for j in range(0, 5):
                        user_name = hotcomments[j]['user']['nickname']
                        user_comment = hotcomments[j]['content']
                        like = hotcomments[j]['likedCount']
                        contents = str(user_name) + ': ' + user_comment + ' ' + str(like)
                        results = results + '\n\n' + contents

                    results = highpoints.sub(u'', results)

                    sql.insert_comments(my_music_name, my_artist_name, comments['total'], results, connection0)
            except Exception as e:
                # 打印错误日志
                print(my_music_id)
                print(e)
                time.sleep(5)


    music_all = sql.get_all_music()



    connection1 = pymysql.connect(host='localhost',
                                  user='root',
                                  password='123456',
                                  db='wangyi2',
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)



    t1 = threading.Thread(target=save_comments, args=(music_all, True, connection1))

    t1.start()

