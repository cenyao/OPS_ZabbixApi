#!/usr/bin/env python3
# -*- encoding: utf8 -*-

from api.zabbix import Zabbix

'''
available : Availability of Zabbix agent. 
    Possible values are:
    0 - (default) unknown;
    1 - available;
    2 - unavailable.
status	: Status and function of the host. 
    Possible values are:
    0 - (default) monitored host;
    1 - unmonitored host.
'''

result_data = {}


def is_monitor(host_ip):
    result_data['api'] = "根据ip查询是否有对应的监控"
    hsotget_json = {
        "method": "host.get",
        "params": {
            "output": "extend",
            "search": {
                "ip": host_ip
            },
            "sortfield": "host"
        }
    }
    _host = Zabbix(hsotget_json).api_post()
    # print(_host)
    if _host:
        hsotinterfaceget_json = {
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "hostids": _host[0]['hostid']
            }
        }
        host_interface = Zabbix(hsotinterfaceget_json).api_post()
        # print(host_interface)
        interface_ip = host_interface[0]['ip']
        if interface_ip == host_ip:
            # print("根据ip(%s)查询到有监控！" % host_ip)
            result_data['result'] = _host[0]
            result_data['status'] = True
        else:
            # print("根据ip(%s)没有找到监控！" % host_ip)
            result_data['result'] = "host_ip跟对应的agent_ip不一致！"
            result_data['status'] = False
    else:
        result_data['result'] = "根据ip(%s)没有找到监控！" % host_ip
        result_data['status'] = False
    return result_data


def host_status(host_ip):
    _host = is_monitor(host_ip)
    # print(_host)
    result_data['api'] = "根据ip查询监控主机的状态"
    if _host['status']:
        if int(_host['result']['maintenance_status']) == 1:
            result_data['result'] = "维护中"
            result_data['status'] = True
            # print("根据ip(%s)查询到对应主机的监控状态是[%s]！" % (host_ip, status))
        else:
            result_data['result'] = _host['result']['status']
            result_data['status'] = True
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data


def host_delect(host_ip):
    _host = is_monitor(host_ip)
    # print(_host)
    result_data['api'] = "根据ip删除对应的监控"
    if _host['status']:
        status = _host['result']['status']
        if int(status) == 1:
            hostdelect_json = {
                "method": "host.delete",
                "params": [
                    _host['result']['hostid']
                ]
            }
            host = Zabbix(hostdelect_json).api_post()
            if host:
                # print("根据ip(%s)已删除该监控！" % host_ip)
                result_data['result'] = "根据ip(%s)已删除该监控！" % host_ip
                result_data['status'] = True
            else:
                result_data['result'] = "根据ip(%s)删除对应的监控失败！" % host_ip
                result_data['status'] = False
        else:
            # print("根据ip(%s)，查询到对应主机agent还在运行，不能删除监控项，请关闭agent并将监控主机状态设置为停用后再删除监控项！" % host_ip)
            result_data['result'] = "根据ip(%s)查询到对应主机状态为启用，不能删除监控项！" % host_ip
            result_data['status'] = False
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data


def hoststatus_update(host_ip, status):
    _host = is_monitor(host_ip)
    # print(_host)
    result_data['api'] = "根据ip修改对应监控主机的监控状态"
    if _host['status']:
        _status = _host['result']['status']
        if _status != status:
            hostdelect_json = {
                "method": "host.update",
                "params": {
                    "hostid": _host['result']['hostid'],
                    "status": status
                }
            }
            host = Zabbix(hostdelect_json).api_post()
            if host:
                result_data['result'] = "已将ip(%s)对应监控主机的状态更改为(%s)！" % (host_ip, status)
                result_data['status'] = True
            else:
                result_data['result'] = '根据ip(%s)修改对应主机的监控状态失败！' % host_ip
                result_data['status'] = False
        else:
            result_data['result'] = '根据ip(%s)查询到对应主机状态和要修改的状态值一致！' % host_ip
            result_data['status'] = False
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data


def hostname_update(host_ip, host_name):
    _host = is_monitor(host_ip)
    result_data['api'] = "根据ip修改对应监控主机的名称"
    if _host['status']:
        hostupdate_json = {
            "method": "host.update",
            "params": {
                "hostid": _host['result']['hostid'],
                "name": host_name
            }
        }
        host = Zabbix(hostupdate_json).api_post()
        if host:
            # print("已将ip(%s)对应监控主机的名称更改为(%s)！" % (host_ip, host_name))
            result_data['result'] = '已将ip(%s)对应监控主机的名称更改为(%s)！' % (host_ip, host_name)
            result_data['status'] = True
        else:
            result_data['result'] = '根据ip(%s)修改对应主机的名称失败！' % host_ip
            result_data['status'] = False
    else:
        result_data['result'] = _host['result']
        result_data['status'] = False
    return result_data


def is_hostgroup(hostgroup_name):
    result_data['api'] = "根据名称查询是否有对应的主机群组"
    hostgroupget_json = {
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    hostgroup_name
                ]
            }
        }
    }
    _hostgroup = Zabbix(hostgroupget_json).api_post()
    if _hostgroup:
        # print("根据名称(%s)查询到有对应的主机群组！" % hostgroup_name)
        result_data['result'] = _hostgroup[0]
        result_data['status'] = True
    else:
        result_data['result'] = '根据名称(%s)没有查询到对应的主机群组！' % hostgroup_name
        result_data['status'] = False
    return result_data
