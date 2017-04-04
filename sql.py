# -*- encoding: utf-8 -*-
"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='wangyi2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# 保存评论
def insert_comments(music_name, artist_name, comments, detail, connection0):
    with connection0.cursor() as cursor:
        sql = "INSERT INTO `comments` (`MUSIC_NAME`, `ARTIST_NAME`, `COMMENTS`, `DETAILS`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (music_name, artist_name, comments, detail))
    connection0.commit()


# 保存音乐
def insert_music(music_id, music_name, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `ARTIST_NAME`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (music_id, music_name, artist_name))
    connection.commit()




# 保存歌手
def insert_artist(artist_id, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (%s, %s)"
        cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `ARTIST_ID`, `ARTIST_NAME` FROM `artists` ORDER BY ARTIST_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()



# 获取所有音乐的 ID
def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID`, `MUSIC_NAME`, `ARTIST_NAME` FROM `musics` ORDER BY MUSIC_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


def dis_connect():
    connection.close()
