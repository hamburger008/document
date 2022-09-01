```
把/home内容备份，然后将/home文件系统所在的逻辑卷删除，扩大/root文件系统，新建/home ，恢复/home内容

1.查看分区

df -h

2.备份home分区文件

tar cvf /tmp/home.tar /home

3.卸载/home，如果无法卸载，先终止使用/home文件系统的进程

fuser -km /home/（没有命令则安装yum install -y psmisc）

umount /home

4.删除/home所在的lv

Lvremove /dev/mapper/centos-home （没有命令则安装yum install device-mappe）

5.扩展/root所在的lv，增加1200G

lvextend -L +1200G /dev/mapper/centos-root

6.扩展/root文件系统

xfs_growfs /dev/mapper/centos-root

7.重新创建home 剩余空间创建新的home

lvcreate -L 200G -n /dev/mapper/centos-home

8. 创建文件系统

mkfs.xfs  /dev/mapper/centos-home

9.挂载home

mount /dev/mapper/centos-home

10.home文件恢复

tar xvf /tmp/home.tar -C /home/

cd /home/home/

mv * ../
```

非 lvm 卷

```
fdisk /dev/sda

P

d


p

1

w

xfs_growfs /dev/sda1
ext4 文件系统 resize2fs /dev/sda1
```

