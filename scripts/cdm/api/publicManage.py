#!usr/bin/env/ python
# -*- coding:utf-8 -*-
# __author__:

import json
import time
import os, sys
p = os.path.dirname(os.path.realpath(__file__))
sys.path.append(p)
from userManage import login


class publicManage(login):
    def add_license(self, code):
        # 添加license
        data = {"licenseCode": code}
        res = self.s.post(self.url + '/oauths/licenses', headers=self.header, json=data)
        return json.loads(res.text)

    def get_license(self):
        # 获取license
        data = {"count": 15, "index": 0}
        res = self.s.get(self.url + '/oauths/licenses', headers=self.header, params=data)
        return json.loads(res.text)

    def active_license(self, code, acode):
        # 激活license
        cid = [x['id'] for x in self.get_license()['responseData']['data'] if x['licenseCode'] == code][0]
        data = {"activeCode": acode}
        res = self.s.post(self.url + '/oauths/license/' + cid + '/active', headers=self.header, json=data)
        return json.loads(res.text)

    def license_cap(self):
        # 获取license容量
        res = self.s.get(self.url + '/oauths/license/overview', headers=self.header)
        return json.loads(res.text)

    def license_cap_abc(self):
        # 获取abc_license容量
        userid = self.get_user_id()
        res = self.s.get(self.url + '/oauths/user/' + userid + '/cloud_license', headers=self.header)
        return json.loads(res.text)

    def del_license(self, code):
        # 删除license
        cid = [x['id'] for x in self.get_license()['responseData']['data'] if x['licenseCode'] == code][0]
        res = self.s.delete(self.url + '/oauths/license/' + cid, headers=self.header)
        return json.loads(res.text)

    def get_node(self):
        # 获取节点信息
        res = self.s.get(self.url + '/clusters/nodes', headers=self.header)
        return json.loads(res.text)

    def add_transferip(self, nodeIp, transferIp, type):
        # 添加传输IP
        nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        data = {"dataTransferIpType": type, "nodeId": nodeId, "ipList": [transferIp]}
        res = self.s.post(self.url + '/storageresmgm/datatransferips', headers=self.header, json=data)
        return json.loads(res.text)

    def get_transferip(self, nodeIp, type):
        # 获取传输IP
        nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        data = {"dataTransferIpType": type, "nodeId": nodeId}
        res = self.s.get(self.url + '/storageresmgm/datatransferips', headers=self.header, params=data)
        return json.loads(res.text)

    def del_transferip(self, nodeIp, transferIp, type):
        # 删除传输IP
        nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        # res0 = self.s.get(self.url + '/storageresmgm/datatransferips', headers=self.header, params={"nodeId": nodeId})
        transferId = [x['id'] for x in self.get_transferip(nodeIp, type)['responseData']['data'] if x['ip'] == transferIp][0]
        data = {"id": transferId, "nodeId": nodeId}
        res = self.s.delete(self.url + '/storageresmgm/datatransferips', headers=self.header, params=data)
        return json.loads(res.text)

    def up_transferip(self, nodeIp, transferIp, type, newIp):
        # 更新传输IP
        nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        # res0 = self.s.get(self.url + '/storageresmgm/datatransferips', headers=self.header, params={"nodeId": nodeId})
        transferId = [x['id'] for x in self.get_transferip(nodeIp, type)['responseData']['data'] if x['ip'] == transferIp][0]
        data = {"id": transferId, "nodeId": nodeId, "newIp": newIp, "dataTransferIpType": type}
        res = self.s.put(self.url + '/storageresmgm/datatransferips', headers=self.header, json=data)
        return json.loads(res.text)

    def get_pools(self):
        # 获取快照池
        # nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        data = {"count": 10, "index": 0}
        res = self.s.get(self.url + '/cdmstores/snapshot_pools', headers=self.header, params=data)
        return json.loads(res.text)

    def up_pools(self, snapshot_pool_id, poolName, mDisks, warnThreshold=90, safeThreshold=95):
        # 修改快照池
        data = {"poolName": poolName, "warnThreshold": warnThreshold, "safeThreshold": safeThreshold, "mDisks": mDisks}
        res = self.s.put(self.url + '/cdmstores/snapshot_pool/' + snapshot_pool_id, headers=self.header, json=data)
        return json.loads(res.text)

    def add_pools(self, nodeIp, name, warnThreshold=90, safeThreshold=95):
        # 添加快照池
        nodeId = [x['id'] for x in self.get_node()['responseData']['data'] if x['nodeIp'] == nodeIp][0]
        data0 = {"filter": True, "nodeIp": nodeIp, "poolId": False}
        res0 = self.s.get(self.url + '/cdmstores/mdisks', headers=self.header, params=data0)
        diskId = [x["diskId"] for x in json.loads(res0.text)["responseData"]][0:1]
        data = {
            "poolName": name,
            "poolId": False,
            "size": 1024,
            "warnThreshold": warnThreshold,
            "safeThreshold": safeThreshold,
            "deviceId": nodeId,
            "mDisks": diskId
        }
        res = self.s.post(self.url + '/cdmstores/snapshot_pools', headers=self.header, json=data)
        return json.loads(res.text)

    def del_pools(self, poolId):
        # 删除快照池
        # poolId = [x['poolId'] for x in self.get_pools()['responseData']['data'] if x['poolName'] == poolName][0]
        data = {"snapshotPoolIds": [poolId]}
        res = self.s.post(self.url + '/cdmstores/snapshot_pools/batch', headers=self.header, json=data)
        return json.loads(res.text)

    def get_clients(self):
        # 获取外接客户端
        data = {
            "clientIsBuildin": "false",
            "count": 15,
            "index": 0,
            "includeSubUser": "true",
            "ifAssign": "",
            "filter": ""
        }
        res = self.s.get(self.url + '/commons/clients', headers=self.header, params=data)
        return json.loads(res.text)

    def distributions(self, ip, user, requestId=""):
        # 分配客户端
        clientId = [x["clientId"] for x in self.get_clients()["responseData"]["data"] if x["clientIp"] == ip]
        data = {"ids": clientId, "userNames": [user], "clientIsBuildin": False, "requestId": requestId, "nodeIp": ""}
        res = self.s.post(self.url + '/oauths/user/clients_distribution', headers=self.header, json=data)
        while not json.loads(res.text)["responseData"]["isFinished"]:
            data["requestId"] = json.loads(res.text)["responseData"]["requestId"]
            res = self.s.post(self.url + '/oauths/user/clients_distribution', headers=self.header, json=data)
        return json.loads(res.text)

    def recover(self, ip, user):
        # 回收客户端
        clientId = [i["clientId"] for i in self.get_clients()["responseData"]["data"] if i["clientIp"] == ip]
        data = {"ids": clientId, "userNames": [user], "clientIsBuildin": False, "requestId": "", "nodeIp": ""}
        res = self.s.post(self.url + '/oauths/user/clients_recover', headers=self.header, json=data)
        while not json.loads(res.text)["responseData"]["isFinished"]:
            data["requestId"] = json.loads(res.text)["responseData"]["requestId"]
            res = self.s.post(self.url + '/oauths/user/clients_recover', headers=self.header, json=data)
        return json.loads(res.text)

    def get_vip(self, type):
        # 获取源端-1/目的端1
        data = {
            "count": 15,
            "index": 0,
            "filter": "",
            "type": type,

        }
        res = self.s.get(self.url + '/clusters/clustermgm/link_clusters', headers=self.header, params=data)
        return json.loads(res.text)

    def add_vip(self, ip):
        # 添加目的端
        data = {
            "destVip": ip
        }
        res = self.s.post(self.url + '/clusters/clustermgm/link_clusters', headers=self.header, json=data)
        return json.loads(res.text)

    def link_vip(self, ip, flag):
        # 目的端同意连接1/取消连接0
        data = {
            "sourceVip": ip,
            "cretify": flag
        }
        res = self.s.post(self.url + '/clusters/clustermgm/certify_cluster', headers=self.header, json=data)
        return json.loads(res.text)

    def get_iqns(self, ip):
        # 获取ISCSI配置
        clientId = [i["clientId"] for i in self.get_clients()["responseData"]["data"] if i["clientIp"] == ip][0]
        res = self.s.get(self.url + '/commons/client/' + clientId + '/iscsi/iqns',
                         headers=self.header, params={"count": 10, "index": 0})
        return json.loads(res.text)

    def get_wwpn(self, ip):
        # 获取FC配置
        clientId = [i["clientId"] for i in self.get_clients()["responseData"]["data"] if i["clientIp"] == ip][0]
        res = self.s.get(self.url + '/commons/client/' + clientId + '/fc/wwpns',
                         headers=self.header, params={"count": 10, "index": 0})
        return json.loads(res.text)

    def add_iqn(self, ip, iqns):
        # 添加ISCSI配置
        clientId = [i["clientId"] for i in self.get_clients()["responseData"]["data"] if i["clientIp"] == ip][0]
        data = {"iqn": iqns, "clientId": clientId}
        res = self.s.post(self.url + '/commons/client/' + clientId + '/iscsi/iqns', headers=self.header, json=data)
        return json.loads(res.text)

    def delete_iqn(self, ip, iqn):
        # 删除ISCSI配置
        iid = [i["id"] for i in self.get_iqns(ip)["responseData"]["data"] if i["iqn"] == iqn][0]
        clientId = [i["clientId"] for i in self.get_clients()["responseData"]["data"] if i["clientIp"] == ip][0]
        res = self.s.delete(self.url + '/commons/client/' + clientId + '/iscsi/iqn/' + iid, headers=self.header)
        return json.loads(res.text)

    def links_create(self, nodeIp, clientIp):
        # 创建链路
        clientList = self.get_clients()["responseData"]["data"]
        clientId = [i["clientId"] for i in clientList if i["clientIp"] == clientIp][0]
        clientName = [i["clientName"] for i in clientList if i["clientIp"] == clientIp][0]
        nodeList = self.get_node()["responseData"]["data"]
        serverId = [i["id"] for i in nodeList if i["nodeIp"] == nodeIp][0]
        serverName = [i["nodeName"] for i in nodeList if i["nodeIp"] == nodeIp][0]
        data = {
            "clientId": clientId,
            "clientIp": clientIp,
            "clientName": clientName,
            "clientOSType": "windows",
            "clientWwn": self.get_iqns(clientIp)["responseData"]["data"][0]["iqn"],
            "fabricType": 1,
            "portalIp": nodeIp,
            "portalPort": "",
            "serverId": serverId,
            "serverName": serverName,
            "serverWwn": "",
            "productType": 1,
        }
        res = self.s.post(self.url + '/storageresmgm/links', headers=self.header, json=data)
        return json.loads(res.text)

    def links_delete(self, nodeIp, linkId):
        # 删除链路
        nodeList = self.get_node()["responseData"]["data"]
        nodeId = [i["id"] for i in nodeList if i["clientIp"] == nodeIp][0]
        data = {
            "nodeId": nodeId,
            "linkId": linkId,
        }
        res = self.s.delete(self.url + '/storageresmgm/links', headers=self.header, params=data)
        return json.loads(res.text)

    def add_vol(self, name, type, size, storageType=0):
        # 创建卷
        nodeList = self.get_node()["responseData"]["data"]
        nodeId = [i["id"] for i in nodeList][0]
        data0 = {"index": 0, "count": 50, "nodeId": nodeId, "type": 1}
        res0 = self.s.get(self.url + '/storageresmgm/storage/path',headers=self.header, params=data0)
        path = json.loads(res0.text)["responseData"]["data"][0]["path"]
        # path = path+"|rm -rf /var/log/anybackup"
        # path = path+";touch /var/log/AnyBackup_2020-09-27-14:12:27/test.txt;"
        # path = "/opt"
        # print(path)
        freeSize = json.loads(res0.text)["responseData"]["data"][0]["freeSize"]
        data = {
            "type": type,
            # "ngDialogId": "ngdialog49",
            "desc": "",
            "name": name,
            "mountPath": path,
            "pathSize": freeSize,
            "storageType": storageType,
            "nodeId": nodeId,
            "size": size
        }
        res = self.s.post(self.url + '/storageresmgm/application/volumes', headers=self.header, json=data)
        return json.loads(res.text)

    def add_vol_raid(self, nodeIp, name, type):
        # 创建卷
        nodeList = self.get_node()["responseData"]["data"]
        nodeId = [i["id"] for i in nodeList if i["nodeIp"] == nodeIp][0]
        data0 = {"index": 0, "count": 15, "nodeId": nodeId, "nodeIp": nodeIp}
        res0 = self.s.get(self.url + '/storageresmgm/raid_volume',headers=self.header, params=data0)
        path = json.loads(res0.text)["responseData"]["data"][0]["raidName"]
        # path = path+"rm -rf /var/log/anybackup"
        # # path = path + ">/var/log/anybackup/1.txt"
        # # path = path+";touch /var/log/AnyBackup_2020-09-27-14:12:27/test.txt;"
        # print(path)
        freeSize = json.loads(res0.text)["responseData"]["data"][0]["raidUsable"]
        data = {
            "type": type,
            # "ngDialogId": "ngdialog49",
            "desc": "",
            "name": name,
            # "mountPath": path,
            # "pathSize": freeSize,
            "storageType": 1,
            "nodeId": nodeId,
            "raidName": path,
            "raidUsable": freeSize,
            "size": 2*1024*1024*1024
        }
        res = self.s.post(self.url + '/storageresmgm/application/volumes', headers=self.header, json=data)
        return json.loads(res.text)

    def get_vol_info(self, type):
        # 获取卷信息
        nodeList = self.get_node()["responseData"]["data"]
        nodeId = [i["id"] for i in nodeList][0]
        data = {
            "count": 15,
            "index": 0,
            "nodeId": nodeId,
            "type": type
        }
        res = self.s.get(self.url + '/storageresmgm/application/volumes', headers=self.header, params=data)
        return json.loads(res.text)

    def del_vol(self, nodeIp, name, type):
        # 删除卷
        volList = self.get_vol_info(nodeIp, type)["responseData"]["data"]
        volId = [i["id"] for i in volList if i["name"] == name][0]
        data = {
            "id": volId
        }
        res = self.s.delete(self.url + '/storageresmgm/application/volumes', headers=self.header, params=data)
        return json.loads(res.text)

    def fingerpoors(self, name, nodeIp):
        # 创建指纹池
        data = {"fpName": name, "nodeIps": [nodeIp], "nodeNum": 1}
        res = self.s.post(self.url + '/commons/fingerpoors', headers=self.header, json=data)
        return json.loads(res.text)

    def del_fingerpoors(self, name):
        # 删除指纹池
        res0 = self.s.get(self.url + '/commons/fingerpoors?count=15&index=0', headers=self.header)
        # print(json.loads(res0.text))
        fpid = [i["fpId"] for i in json.loads(res0.text)["responseData"]["data"] if i["fpName"] == name][0]
        res = self.s.delete(self.url + '/commons/fingerpoors/' + fpid, headers=self.header)
        return json.loads(res.text)

    def distribution_fingerpoors(self, user):
        # 分配指纹池
        res0 = self.s.get(self.url + '/commons/fingerpoors?count=15&index=0', headers=self.header)
        # print(json.loads(res0.text))
        fpid = json.loads(res0.text)["responseData"]["data"][0]["fpId"]
        fpName = json.loads(res0.text)["responseData"]["data"][0]["fpName"]
        data = {"usernames": [user], "fpName": fpName, "fpId": fpid}
        res = self.s.post(self.url + '/oauths/user/fingerpoors_distribution', headers=self.header, json=data)
        return json.loads(res.text)

    def recover_fingerpoors(self, pname, user):
        # 收回指纹池
        res0 = self.s.get(self.url + '/commons/fingerpoors?count=15&index=0', headers=self.header)
        fpid = [i["fpId"] for i in json.loads(res0.text)["responseData"]["data"] if i["fpName"] == pname][0]
        data = {"usernames": [user], "fpName": pname, "fpId": fpid}
        res = self.s.post(self.url + '/oauths/user/fingerpoors_recover', headers=self.header, json=data)
        return json.loads(res.text)

    def fingerlibrary_ab(self, flName, appType):
        # 创建指纹库
        res0 = self.s.get(self.url + '/commons/fingerlibrary/fingerpoors', headers=self.header)
        fpid = json.loads(res0.text)["responseData"]["data"][0]["fpId"]
        fpName = json.loads(res0.text)["responseData"]["data"][0]["fpName"]
        data = {"flName": flName, "appType": appType, "fpGuid": fpid, "fpName": fpName}
        res = self.s.post(self.url + '/commons/fingerprints', headers=self.header, json=data)
        return json.loads(res.text)


    def fingerlibrary_hw(self, flName, appType):
        # 创建指纹库for华为
        data = {"flName": flName, "appType": appType}
        res = self.s.post(self.url + '/commons/fingerprints', headers=self.header, json=data)
        return json.loads(res.text)

    def fingerlibrary_search(self, isAsy=None):
        # 查询指纹库
        data = {"count": 15, "index": 0, "isAsy": isAsy}
        res = self.s.get(self.url + '/commons/fingerprint/search', headers=self.header, params=data)
        return json.loads(res.text)

    def del_fingerlibrary(self, flName):
        # 删除指纹库
        res0 = self.s.get(self.url + '/commons/fingerprints?count=15&flName=&index=0', headers=self.header)
        flGuid = [i["flGuid"] for i in json.loads(res0.text)["responseData"]["data"] if i["flName"] == flName][0]
        res = self.s.delete(self.url + '/commons/fingerprint/' + flGuid, headers=self.header)
        return json.loads(res.text)

    def add_nautilus(self, nodeIp, name, type, size):
        # 创建NAUTILUSDB卷
        nodeList = self.get_node()["responseData"]["data"]
        # print(nodeList)
        nodeId = [i["id"] for i in nodeList if i["nodeIp"] == nodeIp][0]
        poolId = self.get_storage_pool()["responseData"]["data"][0]["id"]
        data = {
            "type": type,
            "desc": "test_y",
            "name": name,
            "storageType": 2,
            "nodeId": nodeId,
            "size": size,
            "poolId": poolId
        }
        res = self.s.post(self.url + '/storageresmgm/application/volumes', headers=self.header, json=data)
        return json.loads(res.text)

    def get_storage_pool(self):
        # 获取存储池
        data = {"index": 0, "count": 15}
        res = self.s.get(self.url + '/storageresmgm/storage/pools', headers=self.header, params=data)
        return json.loads(res.text)

    def create_mdisks(self, nodeIp, size):
        # 创建磁盘
        nodeList = self.get_node()["responseData"]["data"]
        nodeId = [i["id"] for i in nodeList if i["nodeIp"] == nodeIp][0]
        poolId = self.get_storage_pool()["responseData"]["data"][0]["id"]
        data = {
            "nodeId": nodeId,
            "size": size,
            "poolId": poolId
        }
        res = self.s.post(self.url + '/cdmstores/fs_mdisks', headers=self.header, json=data)
        return json.loads(res.text)

    def get_mdisks(self, nodeIp):
        # 获取磁盘
        data = {
            "nodeIp": nodeIp
        }
        res = self.s.get(self.url + '/cdmstores/fs_mdisks', headers=self.header, params=data)
        return json.loads(res.text)

    def del_mdisks(self, diskId):
        # 删除磁盘
        data = {
            "diskId": diskId
        }
        res = self.s.delete(self.url + '/cdmstores/fs_mdisks', headers=self.header, params=data)
        return json.loads(res.text)

    def create_storages(self, name, ip, passwd):
        # 添加存储池
        data = {
            "name": name,
            "ip": ip,
            "port": 28443,
            "userName": "admin",
            "password": passwd,
            "type": 2
        }
        res = self.s.post(self.url + '/storageresmgm/thirdparty/storages', headers=self.header, json=data)
        return json.loads(res.text)

    def get_storages(self):
        # 获取存储池
        res = self.s.get(self.url + '/storageresmgm/thirdparty/storages', headers=self.header)
        storageId = json.loads(res.text)["responseData"]["data"][0]["id"]
        # print(storageId)
        data = {
            "thirdPartyStorageId": storageId
        }
        res = self.s.get(self.url + '/storageresmgm/storage/access/pools', headers=self.header, params=data)
        return json.loads(res.text)

    def add_storages_pool(self):
        # 纳管存储池
        storageId = self.get_storages()["responseData"]["data"][0]["thirdPartyStorageId"]
        name = self.get_storages()["responseData"]["data"][0]["name"]
        data = {"name": name, "thirdPartyStorageId": storageId}
        res = self.s.post(self.url + '/storageresmgm/storage/access/pools', headers=self.header, json=data)
        return json.loads(res.text)

    def get_sla(self):
        # 获取策略信息
        data = {
            "jobType": "eso_backupengine_volumeengine",
            "strategyType": 1,
            "index": 0,
            "count": 15,
        }
        res = self.s.get(self.url + '/commons/sla/strategies', headers=self.header, params=data)
        return json.loads(res.text)

    def create_sla(self, name):
        data = {
            "jobType": "eso_backupengine_volumeengine",
            "strategyName": name,
            "strategyType": 1,
            "dataProtect": {
                "time": 24,
                "unit": 2
            },
            "duration": {
                "enable": 0,
                "time": 1,
                "unit": 6
            },
            "retention": {
                "time": 1,
                "unit": 4
            }
        }
        res = self.s.post(self.url + '/commons/sla/strategies', headers=self.header, json=data)
        return json.loads(res.text)


if __name__ == '__main__':
    #a = publicManage(url="https://192.168.10.10:9600", name='sadmin', password='P@ssword123')
    #a = publicManage(url="https://10.2.155.186:9088", name='admin', password='eisoo.com123')
    a = publicManage(url="https://10.2.238.117:9600", name='admin', password='root1234')
    print(a.add_transferip('192.168.2.30', '192.168.2.30', 0))
    print(a.add_transferip('192.168.2.30', '192.168.2.30', 1))
    print(a.add_transferip('192.168.2.30', '192.168.2.30', 2))   
    #print(a.add_transferip('10.2.155.183', '10.2.155.183'))
    #print(a.add_vol("test02", 10, 70000000000))
    # print(a.add_vol("10.2.10.204", "test00", 1))
    # print(a.del_pools('676ee8ca24bf11eb92b4dc9914004ac1'))
    # a = publicManage(url="https://192.168.10.10:9600", name='audit', password='P@ssword123')
    # print(a.pass_user('P@ssword123', 'eisoo.com123'))
    # print(a.get_sla())
    # print(a.get_storage_pool())
    # print(a.get_transferip('10.2.10.204'))
    # print(a.fingerpoors('pool02', '10.2.10.204'))
    # print(a.distribution_fingerpoors("pool01", "test002"))
    # print(a.fingerlibrary("at01","pool01"))
    # print([i["maps"][0]["usedCapcity"] for i in a.license_cap()["responseData"]["data"]["views"] if i["viewName"]=="后端数据备份容量统计"])
    # print([i['usedCapacity'] for i in a.license_cap_abc()['responseData']['data'] if i['svcType'] == 1])
    # print(a.del_fingerlibrary("at01"))
    # print(a.del_vol('10.2.10.204', 'at003', 1))
    # print(a.delete_iqn('10.2.24.80', 'iqn.1991-05.com.microsoft:win-fp5i6i3nf8n'))
    # print(a.link_vip('10.2.10.206', 0))
    # print(a.del_transferip('10.2.10.204', '10.2.10.204'))
