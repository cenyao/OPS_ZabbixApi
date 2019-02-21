#!/usr/bin/env python3
# -*- encoding: utf8 -*-
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# zabbix的API地址、用户名、密码、这里修改为实际的参数
ZABBIX_URL = "http://192.168.25.100/zabbix/api_jsonrpc.php"
ZABBIX_HEADER = {"Content-Type": "application/json"}
ZABBIX_USER = "Admin"
ZABBIX_PASS = "zabbix"

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'api': 'api.log'
}

# FLASK_HOST = '127.0.0.1'
