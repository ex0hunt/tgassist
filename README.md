AssistBot
=========

Personal assistant (WIP) :)

Current functions
=================
0. Show sys.ifo (with raspberry-pi specific info)
1. Get video link (by webvideo grabber)

Config structure
================
```
$ cat ./config.cfg

[Telegram]
token = <your security token>
admin_id = <user id>
timeout = 10

[Proxy]
address = socks5://<proxy addres>:1080/
username = <proxy user>
password = <proxy password>
```