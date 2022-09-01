https://docs.openstack.org/neutron/latest/admin/config-qos.html

Quality of Service ( QoS )
的qos最终是通过linux tc来实现。可以使用tc命令查看设置是否生效
tc qdisc show dev tap9873a7ae-41
tc filter show dev tap9873a7ae-41 parent ffff:


```
(openvswitch-db)[root@op-144 /]# tc filter ls dev qvob69543cd-92 parent ffff:
filter protocol all pref 49 basic chain 0
filter protocol all pref 49 basic chain 0 handle 0x1
 police 0x1 rate 3Mbit burst 300Kb mtu 64Kb action drop overhead 0b
	ref 1 bind 1
```
fip 限速规则查看


```
[root@op-21 ~]# ip netns exec qrouter-283ec473-22fe-49cd-bb4e-5730ff6c338a  tc filter ls dev qg-0d9c5d21-4e
filter parent 1: protocol ip pref 1 u32 chain 0
filter parent 1: protocol ip pref 1 u32 chain 0 fh 800: ht divisor 1
filter parent 1: protocol ip pref 1 u32 chain 0 fh 800::800 order 2048 key ht 800 bkt 0 flowid :1 not_in_hw
  match 0a10920e/ffffffff at 12
 police 0x1 rate 3Kbit burst 255b mtu 64Kb action drop overhead 0b
	ref 1 bind 1

[root@op-21 ~]#




```
可以从三个方面着手网卡的流量限速。

OVS队列+流表

libvirtd限速接口

Neutron QosPolicy

备注：本文主要采用第1种方式实现限速，简单涉及第2，3种。

OVS队列+流表

```
openvswitch的Port Qos policy只支持HTB
原理如下：

在虚拟机port上创建一条QOS
一条QOS队列对应一条Queue，可以是对应多条Queue
规则OVS通过流表
OpenvSwitch Qos
通过ovs-vsctl show查到虚拟机接到ovs上的tap网卡

#查网卡
$ ovs-vsctl show
5a977fc5-4fdf-4fc7-aea3-a7341a305db1
    Bridge br-int
        fail_mode: secure
        Port "tap53eeb988-c7"
            tag: 4
            Interface "tap53eeb988-c7"
        Port "int-br-bo8eb174"
            Interface "int-br-bo8eb174"
                type: patch
                options: {peer="phy-br-bo8eb174"}
        Port br-int
            Interface br-int
                type: internal
    Bridge br-bond_vmouter
        fail_mode: secure
        Port "phy-br-bo8eb174"
            Interface "phy-br-bo8eb174"
                type: patch
                options: {peer="int-br-bo8eb174"}
        Port bond_vmouter
            Interface bond_vmouter
        Port br-bond_vmouter
            Interface br-bond_vmouter
                type: internal
    ovs_version: "2.5.0"
    
    
#查端口    
$ ovs-ofctl show br-int
FPT_FEATURES_REPLY (xid=0x2): dpid:00005adafb219b49
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
actions: output enqueue set_vlan_vid set_vlan_pcp strip_vlan mod_dl_src mod_dl_dst mod_nw_src mod_nw_dst mod_nw_tos mod_tp_src mod_tp_dst
 1(int-br-bo8eb174): addr:ae:1f:61:28:e4:96
     config:     0
     state:      0
     speed: 0 Mbps now, 0 Mbps max
 9(tap53eeb988-c7): addr:fe:16:3e:e5:d9:00
     config:     0
     state:      0
     current:    10MB-FD COPPER
     speed: 10 Mbps now, 0 Mbps max
 LOCAL(br-int): addr:5a:da:fb:21:9b:49
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0
对tap53eeb988-c7创建一条Qos，其中qos0队列限速最小700Mbps,最大800Mbps

$ ovs-vsctl -- set port tap53eeb988-c7  qos=@newqos \
-- --id=@newqos create qos type=linux-htb other-config:max-rate=800000000 queues=0=@q0 \
-- --id=@q0 create queue other-config:min-rate=700000000 other-config:max-rate=800000000
查当前流表规则

$ ovs-ofctl dump-flows br-int
NXST_FLOW reply (xid=0x4):
 cookie=0xb01c77077412cf51, duration=4216756.364s, table=0, n_packets=390420, n_bytes=36921445, idle_age=0, hard_age=65534, priority=2,in_port=1 actions=drop
 cookie=0xb01c77077412cf51, duration=1554953.959s, table=0, n_packets=620904369, n_bytes=519069450871, idle_age=1, hard_age=65534, priority=9,in_port=19 actions=resubmit(,25)
 cookie=0xb01c77077412cf51, duration=4216750.815s, table=0, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=10,icmp6,in_port=9,icmp_type=136 actions=resubmit(,24)
 cookie=0xb01c77077412cf51, duration=4216750.804s, table=0, n_packets=82396, n_bytes=3460632, idle_age=2242, hard_age=65534, priority=10,arp,in_port=9 actions=resubmit(,24)
 cookie=0xb01c77077412cf51, duration=4216751.878s, table=0, n_packets=1037226147, n_bytes=4734216312377, idle_age=0, hard_age=65534, priority=3,in_port=1,dl_vlan=332 actions=mod_vlan_vid:4,NORMAL
 cookie=0xb01c77077412cf51, duration=4216756.481s, table=0, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=0 actions=NORMAL
 cookie=0xb01c77077412cf51, duration=4216756.473s, table=23, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=0 actions=drop
 cookie=0xb01c77077412cf51, duration=4216750.821s, table=24, n_packets=0, n_bytes=0, idle_age=65534, hard_age=65534, priority=2,icmp6,in_port=9,icmp_type=136,nd_target=fe80::f816:3eff:fee5:d900 actions=NORMAL
 cookie=0xb01c77077412cf51, duration=4216750.809s, table=24, n_packets=82154, n_bytes=3450468, idle_age=2242, hard_age=65534, priority=2,arp,in_port=9,arp_spa=10.16.32.40 actions=resubmit(,25)
 cookie=0xb01c77077412cf51, duration=4216756.466s, table=24, n_packets=1556, n_bytes=65352, idle_age=5669, hard_age=65534, priority=0 actions=drop
 cookie=0xb01c77077412cf51, duration=4215276.624s, table=25, n_packets=1051294240, n_bytes=707172859381, idle_age=20, hard_age=65534, priority=2,in_port=9,dl_src=fa:16:3e:e5:d9:00 actions=NORMAL
从流表里面可以看到通过in_port=9的报文在table 25里面处理，那么问题就很简单了，修改table25，将qos队列规则应用到in_port=9上就可以了，操作如下：

$ ovs-ofctl mod-flows br-int "table=25, n_packets=1051294240, n_bytes=707172859381, idle_age=20, hard_age=65534, priority=2,in_port=9,dl_src=fa:16:3e:e5:d9:00 actions=set_queue:0,NORMAL"
这个时候再观察下虚拟机的监控

限制成功后的虚拟机网卡流量
很好，已经成功限制住了。

那么如何查询qos相关信息呢？

查看网卡属性

$ ovs-vsctl list port tap53eeb988-c7
_uuid               : 4712ae65-bced-4ee3-bf7d-3b7fa1e52bb7
bond_active_slave   : []
bond_downdelay      : 0
bond_fake_iface     : false
bond_mode           : []
bond_updelay        : 0
external_ids        : {}
fake_bridge         : false
interfaces          : [1fe8bb0a-6383-45ba-bc86-46e1de03f4e0]
lacp                : []
mac                 : []
name                : "tap53eeb988-c7"
other_config        : {net_uuid="ea7d53f9-45c6-4027-98b5-23053d10373b", network_type=vlan, physical_network="physnet1", segmentation_id="332", tag="4"}
qos                 : 82bd0134-4e76-405a-ac1d-22b4ea43e55a
rstp_statistics     : {}
rstp_status         : {}
statistics          : {}
status              : {}
tag                 : 4
trunks              : []
vlan_mode           : []
这个82bd0134-4e76-405a-ac1d-22b4ea43e55a就是OVS里面QOS的uuid

查看QOS属性

$ ovs-vsctl list qos 82bd0134-4e76-405a-ac1d-22b4ea43e55a
_uuid               : 82bd0134-4e76-405a-ac1d-22b4ea43e55a
external_ids        : {}
other_config        : {max-rate="800000000"}
queues              : {0=cc4e5d2e-2dbb-4e5b-a682-d6a28bd7b743}
type                : linux-htb
删除QOS并清除网卡QOS

$ ovs-vsctl -- destroy QoS 82bd0134-4e76-405a-ac1d-22b4ea43e55a -- clear Port tap53eeb988 qos
libvirtd限速接口

Libvirtd默认提供domiftune限制网卡流量

查看虚机接口的限速设置

$ virsh  domiftune 4ffbd71f-3324-4500-8636-f9a275b6e479 tap53eeb988
设置虚机接口限速

$ virsh domiftune 4ffbd71f-3324-4500-8636-f9a275b6e479 tap53eeb988 --inbound 700000,800000,800000 --outbount 700000,800000,800000 --live
单位如下

average bandwidth   kilobytes/second 
peak bandwidth      kilobytes/second 
burst size          kilobytes
实际限速值average, 峰值peak和突发值burst是可以合理计算出来的
建议的值:

peak=1.5*average 
burst=peak/8*2=3average/8 
这里要注意的是domiftune只针对网络模式为nat，route等方式，对模型为bridge, passthrough, private,和hostdev是不支持限制的。

The <bandwidth> element allows setting quality of service for a particular network (since 0.9.4). Setting bandwidth for a network is supported only for networks with a <forward> mode of route, nat, or no mode at all (i.e. an "isolated" network). Setting bandwidth is not supported for forward modes of bridge, passthrough, private, or hostdev. Attempts to do this will lead to a failure to define the network or to create a transient network.

Neutron QosPolicy




```





```  
1M 
root@pve:~# tc -s class ls dev veth201i0
class htb 1:1 root prio 0 rate 8388Kbit ceil 8388Kbit burst 1Mb cburst 1598b
 Sent 247291 bytes 2763 pkt (dropped 0, overlimits 1 requeues 0)
 backlog 0b 0p requeues 0
 lended: 2763 borrowed: 0 giants: 0
 tokens: 15624016 ctokens: 22844
 
 
 2m
 
 
root@pve:~# tc -s class ls dev veth201i0
class htb 1:1 root prio 0 rate 16777Kbit ceil 16777Kbit burst 1Mb cburst 1595b
 Sent 1953055 bytes 23308 pkt (dropped 0, overlimits 22 requeues 0)
 backlog 0b 0p requeues 0
 lended: 23308 borrowed: 0 giants: 0
 tokens: 7812008 ctokens: 11414
 
 
 
 3M
 
 root@pve:~# tc -s class ls dev veth201i0
class htb 1:1 root prio 0 rate 25165Kbit ceil 25165Kbit burst 1024Kb cburst 1594b
 Sent 1534717 bytes 19058 pkt (dropped 0, overlimits 15 requeues 0)
 backlog 0b 0p requeues 0
 lended: 19056 borrowed: 0 giants: 0
 tokens: 5208000 ctokens: 7609



4M

root@pve:~# tc -s class ls dev veth201i0
class htb 1:1 root prio 0 rate 33554Kbit ceil 33554Kbit burst 1Mb cburst 1593b
 Sent 1991001 bytes 25126 pkt (dropped 0, overlimits 9 requeues 0)
 backlog 0b 0p requeues 0
 lended: 25126 borrowed: 0 giants: 0
 tokens: 3905834 ctokens: 5537
 
 
 
 
 10M
 
 root@pve:~# tc -s class ls dev veth201i0
class htb 1:1 root prio 0 rate 83886Kbit ceil 83886Kbit burst 1Mb cburst 1593b
 Sent 1944227 bytes 24985 pkt (dropped 0, overlimits 9 requeues 0)
 backlog 0b 0p requeues 0
 lended: 24983 borrowed: 0 giants: 0
 tokens: 1562401 ctokens: 2276

30M

root@pve:~# tc -s class ls dev  veth201i0
class htb 1:1 root prio 0 rate 251658Kbit ceil 251658Kbit burst 1048534b cburst 1541b
 Sent 1847701 bytes 23455 pkt (dropped 0, overlimits 2 requeues 0)
 backlog 0b 0p requeues 0
 lended: 23455 borrowed: 0 giants: 0
 tokens: 520795 ctokens: 748


 ```
