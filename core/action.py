#!/usr/bin/env python3
# -*- encoding: utf8 -*-

from api.zabbix import Zabbix

'''
eventsource: Type of the event. 
    Possible values: 
    0 - event created by a trigger; 
    1 - event created by a discovery rule; 
    2 - event created by active agent auto-registration; 
    3 - internal event.

'''
result_data = {}


def is_autoregistration(autoregistration_name):
    result_data['api'] = "根据名称查询对于的自动注册动作"
    autoregistration_json = {
        "method": "action.get",
        "params": {
            "output": "extend",
            "selectFilter": "extend",
            "filter": {
                "eventsource": 2,
                "name": autoregistration_name
            }
        }
    }
    autoregistration = Zabbix(autoregistration_json).api_post()
    if autoregistration:
        # print("根据名称(%s)查询到有自动注册的动作！" % autoregistration_name)
        result_data['result'] = autoregistration
        result_data['status'] = True
    else:
        # print("根据名称(%s)没有查询到有自动注册的动作！" % autoregistration_name)
        result_data['result'] = "根据名称(%s)没有查询到有自动注册的动作！" % autoregistration_name
        result_data['status'] = False
    return result_data
