# MailME
Mail Notification from Facebook Chatbot API with a mail server help

### main functions
postfix/                -> config for postfix (mysql map)
config.default.py       -> config db, fbtoken
main.py                 -> facebook api webhook handler
requirements.txt        -> python requirements
schema.sql              -> database schema sql
send.py                 -> message send to single user (postfix pipe to here)

### additional tools
broadcast.py            -> broadcast messages to all user subscribe

## installation
* you can put these codes into freebsd jails
* postfix need to support `mysql` map
* setting up facebook api
* setting up postfix/mysql-aliases.cf
* setting up config.py
* run main.py with tmux or screen
