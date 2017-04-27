#zhwnl_mysql_shard_fullback_crontab

#几个脚本介绍
1.mysql_shard_crontab.py
>`1.time_dic这个字典写死了时间与商(day_num)的对应key-value值,不够的话直接添加,现阶段商最大为16,16*7+6=118个主机`
>`2.生成格式为:分钟 小时 星期 主机名`
>`3.没有参数传入为生成mysql_shard_list中得server的crontab时间`
>`4.有一个参数为生成该参数代表server的crontab时间`

2.add_new_to_pylist.sh
>`add_new_to_pylist.sh为使用sed向mysql_shard_list中添加新的主机`

3.add_mysql_shard_crontab.sh
>`add_mysql_shard_crontab.sh直接会再各个主机上生成对应的crontab任务`

4.full_backup.sh
>`全备份脚本`

5.incre_backup.sh
>`增量备份脚本，在每个主机上为每个小时一次`

#zhwnl各个mysql备份时间：

    1 1 * * 0 mysql.shard.2000.m.zhwnl.freed.so
    1 1 * * 1 mysql.shard.2001.m.zhwnl.freed.so
    1 1 * * 2 mysql.shard.2002.m.zhwnl.freed.so
    1 1 * * 3 mysql.shard.2003.m.zhwnl.freed.so
    1 1 * * 4 mysql.shard.2004.m.zhwnl.freed.so
    1 1 * * 5 mysql.shard.2005.m.zhwnl.freed.so
    1 1 * * 6 mysql.shard.2006.m.zhwnl.freed.so
    31 1 * * 0 mysql.shard.2007.m.zhwnl.freed.so
    31 1 * * 1 mysql.shard.2008.m.zhwnl.freed.so
    31 1 * * 2 mysql.shard.2009.m.zhwnl.freed.so
    31 1 * * 3 mysql.shard.2010.m.zhwnl.freed.so
    31 1 * * 4 mysql.shard.2011.m.zhwnl.freed.so
    31 1 * * 5 mysql.shard.2012.m.zhwnl.freed.so
    31 1 * * 6 mysql.shard.2013.m.zhwnl.freed.so
    1 2 * * 0 mysql.shard.2014.m.zhwnl.freed.so
    1 2 * * 1 mysql.shard.2015.m.zhwnl.freed.so
    1 2 * * 2 mysql.shard.2016.m.zhwnl.freed.so
    1 2 * * 3 mysql.shard.2017.m.zhwnl.freed.so
    1 2 * * 4 mysql.shard.2018.m.zhwnl.freed.so
    1 2 * * 5 mysql.shard.2019.m.zhwnl.freed.so
    1 2 * * 6 mysql.shard.2020.m.zhwnl.freed.so
    31 2 * * 0 mysql.shard.2021.m.zhwnl.freed.so
    31 2 * * 1 mysql.shard.2022.m.zhwnl.freed.so
    31 2 * * 2 mysql.shard.2023.m.zhwnl.freed.so
    31 2 * * 3 mysql.shard.2024.m.zhwnl.freed.so
    31 2 * * 4 mysql.shard.2025.m.zhwnl.freed.so
    31 2 * * 5 mysql.shard.2026.m.zhwnl.freed.so
    31 2 * * 6 mysql.shard.2027.m.zhwnl.freed.so
    1 3 * * 0 mysql.shard.2028.m.zhwnl.freed.so
    1 3 * * 1 mysql.shard.2029.m.zhwnl.freed.so
    1 3 * * 2 mysql.shard.2030.m.zhwnl.freed.so
    1 3 * * 3 mysql.shard.2031.m.zhwnl.freed.so
    1 3 * * 4 mysql.shard.2032.m.zhwnl.freed.so
    1 3 * * 5 mysql.shard.2033.m.zhwnl.freed.so
    1 3 * * 6 mysql.shard.2034.m.zhwnl.freed.so
    31 3 * * 0 mysql.shard.2035.m.zhwnl.freed.so
    31 3 * * 1 mysql.shard.2036.m.zhwnl.freed.so
    31 3 * * 2 mysql.shard.2037.m.zhwnl.freed.so
    31 3 * * 3 mysql.shard.2038.m.zhwnl.freed.so
    31 3 * * 4 mysql.shard.2039.m.zhwnl.freed.so
    31 3 * * 5 mysql.shard.2040.m.zhwnl.freed.so
    31 3 * * 6 mysql.shard.2041.m.zhwnl.freed.so
    1 4 * * 0 mysql.shard.2042.m.zhwnl.freed.so
    1 4 * * 1 mysql.shard.2043.m.zhwnl.freed.so
    1 4 * * 2 mysql.shard.2044.m.zhwnl.freed.so
    1 4 * * 3 mysql.shard.2045.m.zhwnl.freed.so
    1 4 * * 4 mysql.shard.2046.m.zhwnl.freed.so
    1 4 * * 5 mysql.shard.2047.m.zhwnl.freed.so
    1 4 * * 6 mysql.shard.2048.m.zhwnl.freed.so
    31 4 * * 0 mysql.shard.2049.m.zhwnl.freed.so
    31 4 * * 1 mysql.shard.2050.m.zhwnl.freed.so
    31 4 * * 2 mysql.shard.2051.m.zhwnl.freed.so
    31 4 * * 3 mysql.shard.2052.m.zhwnl.freed.so
    31 4 * * 4 mysql.shard.2053.m.zhwnl.freed.so


>特殊的几个，用脚本不能生成时间

    1 0 * * 0 mysql.shard.1000.m.zhwnl.freed.so
    1 0 * * 1 mysql.shard.1001.m.zhwnl.freed.so
    1 0 * * 2 mysql.shard.1002.m.zhwnl.freed.so
    1 0 * * 3 mysql.shard.1003.m.zhwnl.freed.so
    1 0 * * 4 mysql.shard.1004.m.zhwnl.freed.so
    1 0 * * 5 mysql.userstore.m.zhwnl.freed.so
    1 0 * * 6 host1.kmzk.freed.so
##others_mysql
    1 0 * * 6 mysql1.lz.freed.so
    25 0 * * 0 mysql.meili.freed.so
    25 0 * * 1 mysql1.pay.freed.so
    25 0 * * 2 mysql1.payment.freed.so
    25 0 * * 3 mysql1.yangmi.freed.so
    25 0 * * 4 mysql1.ym.freed.so
    25 0 * * 5 mysql0.mw.freed.so
    25 0 * * 6 mysql1.pc.freed.so
    45 0 * * 0 mysql1s.pc.freed.so
    45 0 * * 1 mysql2.pc.freed.so
    45 0 * * 2 mysql2s.pc.freed.so
    45 0 * * 3 door.dmp.com(azkban和hive)
