#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import time
from core import host
from api.zabbix import Zabbix

'''
maintenance_from	: Starting time of the effective maintenance.
maintenance_status : Effective maintenance status. 
    Possible values are:
    0 - (default) no maintenance;
    1 - maintenance in effect.
maintenance_type	integer : Effective maintenance type. 
    Possible values are:
    0 - (default) maintenance with data collection;
    1 - maintenance without data collection.
maintenanceid	: ID of the maintenance that is currently in effect on the host.
'''

result_data = {}


def maintenance_status(host_ip):
    _host = host.is_monitor(host_ip)
    # print(_host)
    result_data['api'] = "根据ip查询对应监控主机维护计划的状态"
    maintenanceinfo = {}
    if _host['status']:
        maintenanceinfo['maintenance_status'] = _host['result']['maintenance_status']
        maintenanceinfo['maintenance_type'] = _host['result']['maintenance_type']
        maintenanceinfo['maintenanceid'] = _host['result']['maintenanceid']
        maintenanceinfo['maintenance_from'] = _host['result']['maintenance_from']
        if maintenanceinfo['maintenance_from'] != "0":
            result_data['result'] = maintenanceinfo
            result_data['status'] = True
            # print("根据ip(%s)查询到对应主机的维护状态是[%s]！" % (host_ip, status))
        else:
            result_data['result'] = "根据ip(%s)查询到对应主机没有维护计划！" % host_ip
            result_data['status'] = False
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data


def maintenance_create(host_ip, start_time, end_time):
    _host = host.is_monitor(host_ip)
    # print(_host)
    result_data['api'] = "根据ip新增对应的维护计划"
    if _host['status']:
        status = _host['result']['maintenance_status']
        if status == '0':
            maintenance_name = "%s_%s" % (_host['result']['host'], str(start_time))
            maintenancecreate_json = {
                "method": "maintenance.create",
                "params": {
                    "name": maintenance_name,
                    "active_since": start_time,
                    "active_till": end_time,
                    "maintenance_type": 0,
                    "hostids": [
                        _host['result']['hostid']
                    ],
                    "timeperiods": [
                        {
                            "timeperiod_type": 0,
                            "start_date": start_time,
                            "period": end_time - start_time
                        }
                    ]
                }
            }
            maintenance = Zabbix(maintenancecreate_json).api_post()
            if maintenance:
                # print("根据ip(%s)新增的维护ID是[%s]！" % (host_ip, maintenance['maintenanceids'][0]))
                result_data['result'] = maintenance
                result_data['status'] = True
            else:
                result_data['result'] = '创建维护计划失败！'
                result_data['status'] = False
        else:
            result_data['result'] = "根据ip(%s)查询到对应主机已经有其他的维护计划！" % host_ip
            result_data['status'] = False
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data
