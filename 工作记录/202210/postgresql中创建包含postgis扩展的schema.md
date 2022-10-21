## 需求
工作需要，需要部署一个postgresql的数据库，手里有厂商给的数据库文件

## 经过
通过一系列百度，找到了一个带有postgis扩展的postgresql数据库镜像，放到公司仓库里，k8s部署上

再通过kubectl本地脸上数据库，创建xx数据库后，给的数据库文件里，所有表都是在ziyuan这个schema下，但是创建的数据有个默认schema public

发现postgis提供的函数都是在public中，懵圈了，不知道咋弄了

最好查了一圈资料

通过以下语句，可以修改扩展的所属schema
```sql
create extension extension_name schema schema_name;
alter extension extension_name set schema schema_name;
```

## 坑

数据库连接中指定了currentSchema，发现无效

修改search_path方法

```sql
SET search_path TO itsm;

ALTER database "数据库" SET search_path TO "模式";

## 上门两个我都没成功，用的下面这条语句

alter user “aaaa” set search_path TO "模式";
```


