### 1. 背景
有的时候服务器，有多个网段，默认路由填哪个段哪个段才能和外面通信，但是有时候需要两个段同时与外面通信。

### 2. 修改配置

```python

 echo  "134  vlan134 " >>   /etc/iproute2/rt_tables


[root@hostname ~]# cat  /etc/iproute2/rt_tables
#
# reserved values
#
255	local
254	main
253	default
0	unspec
#
# local
#
#1	inr.ruhep
134  vlan134      ## 仅新增这一行，其他不动
```
```python
# echo "1" > /proc/sys/net/ipv4/ip_forward
ip route flush table vlan134
ip rule add from 10.16.134.0/23  table vlan134
ip route add 0/0 via 10.16.134.1  dev bond1     table 134


打通单个IP

# ip rule add from 10.16.135.37  table vlan134
#  ip route add 0/0 via 10.16.134.1  dev bond1     table 134

####
# ip route add 0/0 via 10.16.134.1  dev bond1  src 10.16.135.37   table 134


```

### 3. 说明

重启网络或者主机重启会还原，需要再配置 rc.local 开启自动配置