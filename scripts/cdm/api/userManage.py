#!usr/bin/env/ python
# -*- coding:utf-8 -*-
# __author__:

import requests
import urllib3
import json
# from readConfig import ReadConfig
import time


class login:
    # config = ReadConfig()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    s = requests.session()

    def __init__(self, url, name, password):
        self.url = url
        self.header = {
            'cache-control': 'no-cache',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'referer': self.url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        data = {
            "userName": name,
            "isEnc": False,
            "userPass": password,
            "validPwdExpire": True
        }
        res = self.s.post(self.url + '/oauths/access_token', headers=self.header, json=data, verify=False)
        # print(res.cookies['csrftoken'])
        self.header['x-csrftoken'] = res.cookies.get('csrftoken')
        # print(res.text)


    def get_user(self, userName, roleType):
        data = {"count": 15, "index": 0, "filterUserName": userName, "roleType": roleType}
        res = self.s.get(self.url + '/oauths/users', params=data, headers=self.header)
        return json.loads(res.text)

    def get_user_id(self):
        res = self.s.get(self.url + '/oauths/profile', headers=self.header)
        return json.loads(res.text)["responseData"]["userInfo"]["userId"]

    def add_user(self, name, type, passwd):
        # role = {"管理员": 0, "租户": 5, "操作员": 3}
        data = {"roleType": type, "userName": name, "isEnc": False, "userPass":passwd, "repeatUserPass":passwd}
        res = self.s.post(self.url + '/oauths/users', headers=self.header, json=data)
        return json.loads(res.text)

    def delete_user(self, id):
        data = {"requestId": "3715a62812bd11eb999f005056828497", "nodeIp": "10.2.10.221", "idSet": [id]}
        res = self.s.post(self.url + '/oauths/users/delete_batch', headers=self.header, json=data)
        return json.loads(res.text)

    def pass_user(self, psw0, psw1):
        user_id = self.get_user_id()
        data = {
            "userId": user_id,
            "oldUserPass": psw0,
            "isEnc": False,
            "repeatUserPass": psw1,
            "userPass": psw1,
        }
        res = self.s.put(self.url + '/oauths/user/'+user_id+'/password', headers=self.header, json=data)
        return json.loads(res.text)

    def login_out(self):
        res = self.s.delete(self.url + '/oauths/access_token', headers=self.header)
        return json.loads(res.text)


if __name__ == '__main__':
    a = login(url='https://192.168.10.10:9600', name='test001', password='P@ssword123')
    # print(a.get_user('admin', 0))
    # print(a.get_user_id())
    print(a.pass_user('P@ssword123', 'eisoo.com123'))
    # name = "test001"
    # print(a.add_user('test001', 5, ""))
    # a = login(url='https://192.168.10.10:9600', name=name, password='Huawei12#$')
    # print(a.pass_user('Huawei12#$', 'eisoo.com123'))
    # a.pass_user("Huawei12#$", "eisoo.com123")
    # print(a.login_out())
