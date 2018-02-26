#!/usr/bin/env python
# -*- encoding: utf8 -*-
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# zabbix的API地址、用户名、密码、这里修改为实际的参数
ZABBIX_URL = "http://192.168.25.100/zabbix/api_jsonrpc.php"
ZABBIX_HEADER = {"Content-Type": "application/json"}
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"

# ZABBIX_URL="http://monitor-1.haowan123.com/api_jsonrpc.php"
# ZABBIX_HEADER = {"Content-Type":"application/json"}
# ZABBIX_USER = "admin"
# ZABBIX_PASS = "!prZiq>H@^>gvW:H<p"

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'api': 'api.log'
}

FLASK_HOST = '0.0.0.0'