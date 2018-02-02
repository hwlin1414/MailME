#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import MySQLdb
import MySQLdb.cursors

import config
import send

db = MySQLdb.connect(
    host = config.DB_HOST,
    user = config.DB_USER,
    passwd = config.DB_PASS,
    db = config.DB_NAME,
    cursorclass=MySQLdb.cursors.DictCursor
)
db.autocommit(True)
cursor = db.cursor()
cursor.execute("set names 'utf8'")

def broadcast_msg(msg):
    cursor.execute("SELECT * FROM `users` WHERE `deleted_at` IS NULL GROUP BY `fid`")
    rows = cursor.fetchall()
    for row in rows:
        send.send_message(row['fid'], msg)

if __name__ == "__main__":
    print("請輸入公告內容：")
    msg = sys.stdin.readlines()
    msg = unicode("".join(msg), "utf-8")
    msg = unicode("[公告]\n", "utf-8") + msg
    broadcast_msg(msg)
