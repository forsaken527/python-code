## umem数据push到open-falcon

### 环境

+ python2

### 运行方式

```python
python umem-to-falcon.py
```

### 修改push的地址

```python
请修改代码中的PUSHURL地址
```

### 部署位置

+ udoor:etouch

```shell
#umem-to-falcon
*/5 * * * *     (cd /data/scripts/cron_scripts/umem-to-falcon; python umem-to-falcon.py ) > /dev/null 2>&1
```
