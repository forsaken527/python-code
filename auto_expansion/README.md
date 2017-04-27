# 据ucloud-api的项目节日提醒自动扩容脚本

### config.py

+ `ucloud API`调用配置:公钥,私钥,API地址等

### create_uhost_instance.py

+ 创建`uhost`
+ 需要在其中配置一些`uhost`的参数
+ 配置详情请参照官方文档：https://docs.ucloud.cn/api/uhost-api/create_uhost_instance

### initialize.sh

+ 初始化脚本
+ 初始化新`uhost`的`peacock`环境

### main-workflow.sh

+ 主要运行脚本
+ 在其中的`sum`配置需要创建的`uhost`个数

###nginx.conf

+ 从`ansible`中拷贝的`nginx`配置文件，不需要最修改

### sdk.py

+ `api`的相关`sdk`方法

### terminate_uhost_Instance.py

+ 调用`api`删除`uhost`的脚本

### back目录

+ 为nginx恢复的时候需要的备份配置文件

# NOTICE
1. 创建的`uhost`为按需付费，如果需要其他类型的，请在`create_uhost_instance.py`中添加官方文档中的对应字段
2. 运行时目录下会生成`id_list`与`id_list`文件，其中写着`ip`地址与`uhost_id`，程序结束后自动删除
3. `terminate_uhost_Instance.py`可以单独使用，`sys.argv[1]` 为需要删除的`uhost`的`uhost_id`
4. `create_uhost_instance.py`可以单独使用
5. 几个修改的原来的发布系统和批量管理`ansible`的地方：

+ /data/etouch/release/wars/peacock_api/release.sh
```shell
    #自动扩容用
    /usr/bin/svn up --username deploy --password 1qa2ws3ed /data/tmp/peacock < $data/release/yes
```

+ /data/etouch/abcm/hosts/main_pc_tc.sh
```shell
    #自动扩容用
    rsync -az $binPath/conf/hosts_$host /data/tmp/peacock/hosts
```
