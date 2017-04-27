# 监控umem的状态并且自动扩容
### 相关工作流程如图所示
![如果无法显示请查看flow_chart.png](http://git.etouch.cn/gitbucket/ssy-SR/ops/blob/master/4%E5%B9%B3%E5%8F%B0-%E5%A4%A7%E5%AE%9D%E5%89%91/umem_monitor_rsize/flow_chart.png)

### get_umem中的一些解释

1.`PHONE_NUMBER`为需要发送报警短信电话号码，多个电话请用逗号隔开

2.`REDIS_HOST`为使用redis的ip地址

3.`REDIS_PORT`为redis端口

4.当前设定的阀值为0.98，即%98，如若需要修改阀值请移至`Threshold`

5.如果需要修改自动扩容次数请移至`TIMES`

## 重要
### `reset.py`使用注意事项

**1. 不使用参数`python reset.py`为重置数据库中所有的umem扩容次数为0**

**2. 使用一个参数`python reset.py umme_name`为重置指定名称的umem的次数为0**
