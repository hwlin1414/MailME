#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import json
from flask import Flask, request
import requests
import MySQLdb
import MySQLdb.cursors

import config
import send

app = Flask(__name__)
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

@app.route(config.WEBHOOK_ROOT, methods=["GET"])
def fb_webhook():
    verify_token = request.args.get('hub.verify_token')
    if config.verification_code == verify_token:
        return request.args.get('hub.challenge')

@app.route(config.WEBHOOK_ROOT, methods=['POST'])
def fb_handle_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        messagings = entry['messaging']
        for message in messagings:
            sender = message['sender']['id']
            if message.get('message'):
                if 'text' in message['message']:
                    text = message['message']['text']
                    print(u"{} says \"{}\"".format(sender, text))
                    app_message(sender, text)
                else:
                    print(u"{} says nothing".format(sender))
                    app_message(sender, '')
    return "Hi"

def app_message(sender, text):
    msgmap = {
        "reg": [u"reg", u"regist", u"註冊", u"訂閱"],
        "unreg": [u"unreg", u"unregist", u"取消", u"取消註冊", u"取消訂閱"],
        "help": [u"help", u"幫助"],
    }
    cmd = text.split()
    if cmd[0] in msgmap['reg']:
        result = re.match('^[a-zA-Z0-9_]{3,24}$', cmd[1])
        if result is None:
            send.send_message(sender, u"註冊電子郵件地址僅能包含英文、數字、_，且須於3~24個字元")
            return
        if cmd[1] in config.RESERVE:
            send.send_message(sender, u"該帳號為保留字")
            return
        cursor.execute(
            "SELECT * FROM `users` WHERE `alias` = %(alias)s AND `fid` != %(fid)s",
            {"fid": sender, "alias": cmd[1]}
        )
        rows = cursor.fetchall()
        if len(rows) != 0:
            send.send_message(sender, u"該帳號已被其他人註冊走囉~")
            return

        cursor.execute(
            "UPDATE `users` SET `deleted_at` = CURRENT_TIMESTAMP() WHERE `fid` = %(fid)s",
            {"fid": sender}
        );
        cursor.execute(
            "INSERT INTO `users`(`fid`, `alias`) VALUE(%(fid)s, %(alias)s)",
            {"fid": sender, "alias": cmd[1]}
        );
        send.send_message(sender, u"註冊成功，您可以開始寄信至 {alias}@mailme.csie.io".format(alias = cmd[1]))
    elif cmd[0] in msgmap['unreg']:
        cursor.execute(
            "UPDATE `users` SET `deleted_at` = CURRENT_TIMESTAMP() WHERE `fid` = %(fid)s",
            {"fid": sender}
        );
        send.send_message(sender, u"已取消註冊")
    elif cmd[0] in msgmap['help']:
        pass
    else:
        send.send_message(sender, u"您好，歡迎使用MailME，請詳閱粉專說明後，輸入\"註冊 XXX\"或\"取消註冊\"")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
