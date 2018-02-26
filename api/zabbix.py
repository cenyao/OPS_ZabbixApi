#!/usr/bin/env python
# -*- encoding: utf8 -*-
import sys
import json
import urllib
from urllib import error
from urllib import request
from conf import settings


class Zabbix(object):
    def __init__(self, json_data):
        self.zabbix_url = settings.ZABBIX_URL
        self.zabbix_header = settings.ZABBIX_HEADER
        self.zabbix_user = settings.ZABBIX_USER
        self.zabbix_pass = settings.ZABBIX_PASS
        self.json_data = json_data

    def get_token(self):
        auth_data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                        "user": self.zabbix_user,
                        "password": self.zabbix_pass
                    },
                "id": 0
            }).encode('utf-8')
        # create request object
        _request = urllib.request.Request(self.zabbix_url, auth_data)
        for key in self.zabbix_header:
            _request.add_header(key, self.zabbix_header[key])
            # 认证和获取SESSION ID
        try:
            result = urllib.request.urlopen(_request)
            # 对于认证出错的处理
        except error.HTTPError as e:
            print('The server couldn\'t fulfill the request, Error code: ', e.code)
        except error.URLError as e:
            print('We failed to reach a server.Reason: ', e.reason)
        else:
            _response = json.loads(result.read())
            return _response

    def api_post(self):
        # 判断SESSIONID是否在返回的数据中
        _token = Zabbix.get_token(self)
        if 'result' in _token:
            auth_code = _token['result']
            # 用得到的SESSIONID去验证
            if len(auth_code) == 0:
                sys.exit(1)

            elif len(auth_code) != 0:
                json_base = {
                    "jsonrpc": "2.0",
                    "auth": auth_code,
                    "id": 1
                }
                self.json_data.update(json_base)
                get_host_data = json.dumps(self.json_data).encode('utf-8')
                # create request object
                _request = urllib.request.Request(self.zabbix_url, get_host_data)
                for key in self.zabbix_header:
                    _request.add_header(key, self.zabbix_header[key])

                # get host list
                try:
                    result = urllib.request.urlopen(_request)
                except error.HTTPError as e:
                    print('The server couldn\'t fulfill the request, Error code: ', e.code)
                except error.URLError as e:
                    print('We failed to reach a server.Reason: ', e.reason)
                else:
                    _response = json.loads(result.read())
                    # print(_response)
                    result.close()
                    # 将所有的主机信息显示出来
                    if 'result' in _response:
                        _result = _response['result']
                        return _result
                    else:
                        print(_response['error'])
                        return False
        else:
            print(_token['error'])
            return False
