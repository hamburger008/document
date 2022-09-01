1. 查找计算节点的 对应的 parent_provider_id 

```bash
MariaDB [nova_api]>  select * from resource_providers;
+---------------------+---------------------+----+--------------------------------------+--------------+------------+----------+------------------+--------------------+
| created_at          | updated_at          | id | uuid                                 | name         | generation | can_host | root_provider_id | parent_provider_id |
+---------------------+---------------------+----+--------------------------------------+--------------+------------+----------+------------------+--------------------+
| 2019-06-06 03:12:25 | 2019-11-20 11:47:59 |  4 | d083af9b-b807-40ce-9e4a-33e5c25297cd | jitstack0002 |        173 |     NULL |                4 |               NULL |
| 2019-06-06 03:12:26 | 2019-11-20 11:49:52 |  7 | 065ae8bf-8297-4df3-9361-34943f1fca4a | jitstack0003 |         71 |     NULL |                7 |               NULL |
| 2019-06-06 03:12:28 | 2019-08-02 08:17:35 | 10 | fd7f516f-4fb9-40c2-9634-94188456a7f9 | jitstack0001 |        201 |     NULL |               10 |               NULL |
+---------------------+---------------------+----+--------------------------------------+--------------+------------+----------+------------------+--------------------+
3 rows in set (0.00 sec)
```

2.通过 resource_provider_id 查找每个计算节点分配的资源

```bash
MariaDB [nova_api]>  select * from nova_api.allocations where resource_provider_id=7;;
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
| created_at          | updated_at | id   | resource_provider_id | consumer_id                          | resource_class_id | used  |
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
| 2019-08-19 05:15:00 | NULL       | 1426 |                    7 | aebbb013-21d1-4bf3-bd94-e91735db7125 |                 0 |     4 |
| 2019-08-23 09:10:59 | NULL       | 1436 |                    7 | 1a7f895b-15bd-4e59-868f-19f7a51becd0 |                 0 |     4 |
| 2019-08-23 09:11:02 | NULL       | 1438 |                    7 | de533a1d-e691-4c61-bd08-3b64d352e1d5 |                 0 |     4 |
| 2019-11-04 08:00:25 | NULL       | 1460 |                    7 | f216f940-a6d7-4f7a-8e8a-b37c7295d768 |                 0 |     4 |
| 2019-06-20 03:24:09 | NULL       |  581 |                    7 | ddd4a5b0-6432-4d57-af8f-8de1c350327e |                 0 |     8 |
| 2019-07-11 03:53:35 | NULL       |  713 |                    7 | 152ee0b0-4030-400f-82e1-20e3eef68e10 |                 0 |     8 |
| 2019-08-15 09:44:22 | NULL       | 1402 |                    7 | d73af926-c8fc-433c-8b00-445d29f43722 |                 0 |     8 |
| 2019-08-16 05:48:07 | NULL       | 1416 |                    7 | 3f6240fb-a022-453f-925c-71aabffbf36c |                 0 |     8 |
| 2019-08-16 05:48:15 | NULL       | 1420 |                    7 | 848b12d2-95b3-4a6f-b303-ea0549f38ff5 |                 0 |     8 |
| 2019-08-16 06:09:49 | NULL       | 1422 |                    7 | 8e1ec578-e690-486c-8ee3-4324a9ec8ec3 |                 0 |     8 |
| 2019-11-20 11:49:52 | NULL       | 1510 |                    7 | 5d5a4ce4-2e65-4783-b42d-65bc7f2cd9d5 |                 0 |     8 |
| 2019-08-19 05:15:00 | NULL       | 1427 |                    7 | aebbb013-21d1-4bf3-bd94-e91735db7125 |                 1 |  4096 |
| 2019-08-23 09:10:59 | NULL       | 1437 |                    7 | 1a7f895b-15bd-4e59-868f-19f7a51becd0 |                 1 |  4096 |
| 2019-08-23 09:11:02 | NULL       | 1439 |                    7 | de533a1d-e691-4c61-bd08-3b64d352e1d5 |                 1 |  4096 |
| 2019-11-20 11:49:52 | NULL       | 1511 |                    7 | 5d5a4ce4-2e65-4783-b42d-65bc7f2cd9d5 |                 1 |  4096 |
| 2019-11-04 08:00:25 | NULL       | 1461 |                    7 | f216f940-a6d7-4f7a-8e8a-b37c7295d768 |                 1 |  8192 |
| 2019-06-20 03:24:09 | NULL       |  583 |                    7 | ddd4a5b0-6432-4d57-af8f-8de1c350327e |                 1 | 16384 |
| 2019-08-15 09:44:22 | NULL       | 1403 |                    7 | d73af926-c8fc-433c-8b00-445d29f43722 |                 1 | 16384 |
| 2019-08-16 05:48:07 | NULL       | 1417 |                    7 | 3f6240fb-a022-453f-925c-71aabffbf36c |                 1 | 32768 |
| 2019-08-16 05:48:15 | NULL       | 1421 |                    7 | 848b12d2-95b3-4a6f-b303-ea0549f38ff5 |                 1 | 32768 |
| 2019-08-16 06:09:49 | NULL       | 1423 |                    7 | 8e1ec578-e690-486c-8ee3-4324a9ec8ec3 |                 1 | 32768 |
| 2019-07-11 03:53:35 | NULL       |  715 |                    7 | 152ee0b0-4030-400f-82e1-20e3eef68e10 |                 1 | 65536 |
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
22 rows in set (0.00 sec)
```

3. 查找现在 openstack  nova.instances 运行的的实际虚拟机 （暂不考虑 KVM 和 OpenStack 不同步情况）

```bash
MariaDB [nova_api]> select uuid from nova.instances where deleted=0 and node='jitstack0001';
+--------------------------------------+
| uuid                                 |
+--------------------------------------+
| 1625ce70-5745-4b3b-87bf-6d590144d824 |
| ea68349f-d00b-41bb-9573-9610ca8392ad |
| 2b3d6dfa-893b-47cc-a9f2-727b54827b40 |
| a1aa8ae2-dc1e-45c1-866b-5f250dfe6922 |
| 878fd818-f22f-488d-9a26-27c58fef9e04 |
| 08a0bc35-90ae-496b-889c-6d9261573fef |
| 446d9d2c-629e-40bc-a8b2-74f4d01643fc |
| f1d94dd7-7f25-43a4-b4e6-40f76a8ed3ec |
| caafea14-2388-463d-96fe-a55a7327a0ad |
+--------------------------------------+
9 rows in set (0.00 sec)
```



4.按照 nova.instances 表为准，删除 nova_api.allocations 表中多余的记录

```bash
delete from nova_api.allocations where consumer_id='$consumer_id' and resource_provider_id=$resource_provider_id;
```







#### 版本不一样数据库结构可能不一样

S版本为例


查看每个计算节点对应的 ID
```

 MariaDB [(none)]>  select * from placement.resource_providers;
+---------------------+---------------------+-----+--------------------------------------+--------------------------------------+------------+------------------+--------------------+
| created_at          | updated_at          | id  | uuid                                 | name                                 | generation | root_provider_id | parent_provider_id |
+---------------------+---------------------+-----+--------------------------------------+--------------------------------------+------------+------------------+--------------------+
| 
| 2020-06-28 10:04:25 | 2022-02-15 05:37:55 |  25 | a0b85dd0-b0c4-4964-a867-c0aaf1348451 | openstack55                          |        191 |               25 |               NULL |
| 2020-06-28 10:04:25 | 2022-03-03 01:46:33 |  28 | d2e6b83b-3380-45a2-8603-9971e17878e9 | openstack45                          |        233 |               28 |               NULL |
| 2022-03-02 09:22:41 | 2022-03-03 03:01:51 | 883 | 2c5372fb-828b-43de-bb52-09401d6f00f4 | openstack61                          |         17 |              883 |               NULL |
+---------------------+---------------------+-----+--------------------------------------+--------------------------------------+------------+------------------+--------------------+

```
查看计算节点openstack61(883),记录的分配资源情况

0代表CPU 1代表内存，2代表磁盘

```
MariaDB [(none)]>  select * from placement.allocations  where resource_provider_id=883;
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
| created_at          | updated_at | id   | resource_provider_id | consumer_id                          | resource_class_id | used  |
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
| 2022-03-03 01:43:51 | NULL       | 9679 |                  883 | 9caf317d-9433-4055-96bf-c65bfd1d8fb2 |                 0 |     8 |
| 2022-03-03 01:46:42 | NULL       | 9697 |                  883 | a1c57e94-e626-4ffe-a72d-3f33164b0f81 |                 0 |     8 |
| 2022-03-03 03:01:51 | NULL       | 9787 |                  883 | a149ea55-faf2-43b0-abc1-2aa84e522da5 |                 0 |     8 |
| 2022-03-03 01:43:51 | NULL       | 9676 |                  883 | 9caf317d-9433-4055-96bf-c65bfd1d8fb2 |                 1 | 16384 |
| 2022-03-03 01:46:42 | NULL       | 9694 |                  883 | a1c57e94-e626-4ffe-a72d-3f33164b0f81 |                 1 | 16384 |
| 2022-03-03 03:01:51 | NULL       | 9784 |                  883 | a149ea55-faf2-43b0-abc1-2aa84e522da5 |                 1 | 32768 |
| 2022-03-03 01:43:51 | NULL       | 9682 |                  883 | 9caf317d-9433-4055-96bf-c65bfd1d8fb2 |                 2 |    40 |
| 2022-03-03 01:46:42 | NULL       | 9700 |                  883 | a1c57e94-e626-4ffe-a72d-3f33164b0f81 |                 2 |    40 |
| 2022-03-03 03:01:51 | NULL       | 9790 |                  883 | a149ea55-faf2-43b0-abc1-2aa84e522da5 |                 2 |    40 |
+---------------------+------------+------+----------------------+--------------------------------------+-------------------+-------+
```

查看计算节点上面未被删除的虚拟机

```
MariaDB [(none)]>  select uuid  from nova.instances  where deleted=0  and  node='openstack61';
+--------------------------------------+
| uuid                                 |
+--------------------------------------+
| 9caf317d-9433-4055-96bf-c65bfd1d8fb2 |
+--------------------------------------+
1 row in set (0.001 sec)

MariaDB [(none)]>

```




#####  port 也有残留情况


```
MariaDB [neutron]> select * from neutron.ml2_port_binding_levels where port_id="6eaef455-c2d5-4a76-a8ac-53d7e5d65515";
+--------------------------------------+-------------+-------+-------------+--------------------------------------+
| port_id                              | host        | level | driver      | segment_id                           |
+--------------------------------------+-------------+-------+-------------+--------------------------------------+
| 6eaef455-c2d5-4a76-a8ac-53d7e5d65515 | openstack45 |     0 | openvswitch | ac46216e-32ab-4643-9899-3237e8f4f974 |
| 6eaef455-c2d5-4a76-a8ac-53d7e5d65515 | openstack61 |     0 | openvswitch | ac46216e-32ab-4643-9899-3237e8f4f974 |
| 6eaef455-c2d5-4a76-a8ac-53d7e5d65515 | openstack81 |     0 | openvswitch | ac46216e-32ab-4643-9899-3237e8f4f974 |
+--------------------------------------+-------------+-------+-------------+--------------------------------------+

MariaDB [(none)]> select * from neutron.ml2_port_bindings where port_id="6eaef455-c2d5-4a76-a8ac-53d7e5d65515";
+--------------------------------------+-------------+----------+-----------+---------+----------------------------------------------------------------------------------------------------+----------+
| port_id                              | host        | vif_type | vnic_type | profile | vif_details                                                                                        | status   |
+--------------------------------------+-------------+----------+-----------+---------+----------------------------------------------------------------------------------------------------+----------+
| 6eaef455-c2d5-4a76-a8ac-53d7e5d65515 | openstack45 | ovs      | normal    |         | {"port_filter": true, "bridge_name": "br-int", "datapath_type": "system", "ovs_hybrid_plug": true} | ACTIVE   |
| 6eaef455-c2d5-4a76-a8ac-53d7e5d65515 | openstack61 | ovs      | normal    |         | {"port_filter": true, "bridge_name": "br-int", "datapath_type": "system", "ovs_hybrid_plug": true} | INACTIVE |
+--------------------------------------+-------------+----------+-----------+---------+----------------------------------------------------------------------------------------------------+----------+
2 rows in set (0.000 sec)


删除语句
delete from  neutron.ml2_port_binding_levels where port_id="6eaef455-c2d5-4a76-a8ac-53d7e5d65515" and host="openstack61"


```




####  volume 可能也有残留

```
MariaDB [(none)]> select * from cinder.volume_attachment  where volume_id="7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd" and deleted=0\G
*************************** 1. row ***************************
     created_at: 2022-03-03 15:09:21
     updated_at: 2022-03-03 15:09:25
     deleted_at: NULL
        deleted: 0
             id: 17f7170f-ad4f-404a-959a-85a3a3702897
      volume_id: 7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd
  attached_host: openstack81
  instance_uuid: 74181f33-598a-4a16-b72d-3ae25d23758e
     mountpoint: /dev/vdb
    attach_time: 2022-03-03 15:09:07
    detach_time: NULL
    attach_mode: null
  attach_status: attached
connection_info: {"attachment_id": "17f7170f-ad4f-404a-959a-85a3a3702897", "encrypted": false, "driver_volume_type": "rbd", "secret_uuid": "4ef7a9d3-d7e8-4487-9790-e6e4e4502cf6", "qos_specs": null, "volume_id": "7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd", "auth_username": "cinder", "secret_type": "ceph", "name": "volumes/volume-7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd", "discard": true, "keyring": null, "cluster_name": "ceph", "auth_enabled": true, "hosts": ["10.16.134.16", "10.16.134.17", "10.16.134.37"], "access_mode": "rw", "ports": ["6789", "6789", "6789"]}
      connector: {"initiator": "iqn.1994-05.com.redhat:2426835eb68", "ip": "10.16.140.81", "system uuid": "14D9FBDC-37B7-11E9-9AD0-70C7F2DB52BA", "platform": "x86_64", "host": "openstack81", "mode": null, "do_local_attach": false, "mountpoint": "/dev/vdb", "os_type": "linux2", "multipath": false}
*************************** 2. row ***************************
     created_at: 2021-01-14 07:09:06
     updated_at: 2021-01-14 07:09:07
     deleted_at: NULL
        deleted: 0
             id: 8b65a1dc-6fc2-4600-9d8d-7b473ca108cb
      volume_id: 7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd
  attached_host: openstack45
  instance_uuid: 74181f33-598a-4a16-b72d-3ae25d23758e
     mountpoint: /dev/vdb
    attach_time: 2021-01-14 07:09:07
    detach_time: NULL
    attach_mode: rw
  attach_status: attached
connection_info: {"attachment_id": "8b65a1dc-6fc2-4600-9d8d-7b473ca108cb", "encrypted": false, "driver_volume_type": "rbd", "secret_uuid": "4ef7a9d3-d7e8-4487-9790-e6e4e4502cf6", "qos_specs": null, "volume_id": "7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd", "auth_username": "cinder", "secret_type": "ceph", "name": "volumes/volume-7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd", "discard": true, "keyring": null, "cluster_name": "ceph", "auth_enabled": true, "hosts": ["10.16.134.16", "10.16.134.17", "10.16.134.37"], "access_mode": "rw", "ports": ["6789", "6789", "6789"]}
      connector: {"initiator": "iqn.1994-05.com.redhat:2426835eb68", "ip": "10.16.140.45", "system uuid": "B214F03E-36FC-11E9-8416-04885FA5DBB6", "platform": "x86_64", "host": "openstack45", "do_local_attach": false, "mountpoint": "/dev/vdb", "os_type": "linux2", "multipath": false}
2 rows in set (0.003 sec)

MariaDB [(none)]>
MariaDB [(none)]>
MariaDB [(none)]> delete from cinder.volume_attachment  where volume_id="7b0eea9b-50fd-4af5-b80d-4d300bdd7ecd" and attached_host="openstack81";
Query OK, 1 row affected (0.001 sec)

MariaDB [(none)]>
```
