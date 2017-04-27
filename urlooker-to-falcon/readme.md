# urlooker-to-falcon

## rlooker-to-falcon.py

### python version
 + 2.x
 
### configuration
```conf
PUSHHOME="http://123.59.43.96:1988/v1/push"
HOST=""  # host
ZoneTag = ""  # zone
PORT=3306   # mysql port
USER='root'   # mysql user
PASSWD=""     # password
DB='urlooker'  # database
```

### deploy
 + crontab
 ```crontab
*/5 * * * * (cd /home;python urlooker-to-falcon.py)
```

### falcon push api
 + `http://123.59.43.96:1988/v1/push`


