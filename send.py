#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import config
import email
import email.parser
import email.header
import requests
import json

EX_TEMPFAIL=75
EX_UNAVAILABLE=69

def send_message(to, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token = config.FB_TOKEN)
    response_message = json.dumps({"recipient":{"id": to}, 
                                   "message":{"text":message}})
    req = requests.post(post_message_url, 
                        headers={"Content-Type": "application/json"}, 
                        data=response_message)
    if __name__ != "__main__":
        print(u"[{}] Reply to {}: {}".format(req.status_code, to, message))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s FID" % (sys.argv[0]))
        sys.exit(EX_TEMPFAIL)
    
    mail = ''.join(sys.stdin.readlines())
    parser = email.parser.Parser()
    
    content = parser.parsestr(mail)
    mf = email.header.decode_header(content["From"])[0][0]
    sj = email.header.decode_header(content["Subject"])[0][0]
    mailfrom = unicode(mf, errors='replace')
    subject = unicode(sj, errors='replace')
    try:
        mailfrom = mf.decode('UTF-8')
        subject = sj.decode('UTF-8')
    except:
        try:
            mailfrom = mf.decode('BIG5')
            subject = sj.decode('BIG5')
        except:
            pass
    data = u"""
[通知]
來自: {mailfrom}
主旨: {subject}
""".format(mailfrom = mailfrom, subject = subject)
    
    #if content.is_multipart():
    #    for payload in content.get_payload():
    #        if payload.get_content_type() == 'text/plain':
    #            data += unicode(payload.get_payload(decode = True), errors='replace')
    #elif content.get_content_type() == 'text/plain':
    #    data += unicode(content.get_payload(decode = True), errors='replace')

    send_message(sys.argv[1], data)
