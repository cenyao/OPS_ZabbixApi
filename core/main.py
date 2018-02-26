#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import time
from flask import Flask, jsonify
from flask import request, abort, make_response
from core import host
from core import maintenance
from core import action
from core import logger

api_logger = logger.logger('api')
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
error_info = {
    'result': '',
    'status': ''
}


@app.errorhandler(400)
def postdata_error(error):
    error_info['result'] = 'Post data error!'
    error_info['status'] = False
    return make_response(jsonify(error_info), 400)


@app.errorhandler(404)
def not_found(error):
    error_info['result'] = 'Not found!'
    error_info['status'] = False
    return make_response(jsonify(error_info), 404)


@app.errorhandler(405)
def postdata_error(error):
    error_info['result'] = 'Post data error!'
    error_info['status'] = False
    return make_response(jsonify(error_info), 405)


@app.errorhandler(500)
def process_error(error):
    error_info['result'] = 'Process error!'
    error_info['status'] = False
    return make_response(jsonify(error_info), 500)


@app.route('/api/v1.0/host/is_monitor', methods=['POST'])
def host_ismonitor():
    if not request.json or 'host_ip' not in request.json:
        abort(405)
    host_ip = request.json['host_ip']
    _host = host.is_monitor(host_ip)
    if _host['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    return jsonify(_host)


@app.route('/api/v1.0/host/host_status', methods=['POST'])
def host_status():
    if not request.json or 'host_ip' not in request.json:
        abort(405)
    host_ip = request.json['host_ip']
    _host = host.host_status(host_ip)
    if _host['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    return jsonify(_host)


@app.route('/api/v1.0/host/host_delete', methods=['POST'])
def host_delete():
    if not request.json or 'host_ip' not in request.json:
        abort(405)
    host_ip = request.json['host_ip']
    _host = host.host_delect(host_ip)
    if _host['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    return jsonify(_host)


@app.route('/api/v1.0/host/hoststatus_update', methods=['POST'])
def hoststatus_update():
    if not request.json or 'host_ip' not in request.json or 'host_status' not in request.json:
        abort(405)
    data = {}
    host_ip = request.json['host_ip']
    status = request.json['host_status']
    if int(status) not in [0, 1]:
        data['result'] = "监控主机的状态只能是0或者1！"
        data['status'] = False
        data['api'] = "根据ip修改对应监控主机的监控状态"
        return jsonify(data)
    _host = host.hoststatus_update(host_ip, status)
    if _host['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    return jsonify(_host)


@app.route('/api/v1.0/host/hostname_update', methods=['POST'])
def hostname_update():
    if not request.json or 'host_ip' not in request.json or 'host_name' not in request.json:
        abort(405)
    host_ip = request.json['host_ip']
    host_name = request.json['host_name']
    _host = host.hostname_update(host_ip, host_name)
    if _host['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_host['api'], host_ip, _host['status']))
    return jsonify(_host)


@app.route('/api/v1.0/hostgroup/is_hostgroup', methods=['POST'])
def is_hostgroup():
    if not request.json or 'hostgroup_name' not in request.json:
        abort(405)
    hostgroup_name = request.json['hostgroup_name']
    _hostgroup = host.is_hostgroup(hostgroup_name)
    if _hostgroup['status']:
        api_logger.info("Api:[%s] Name:[%s] Result:[%s]" % (_hostgroup['api'], hostgroup_name, _hostgroup['status']))
    else:
        api_logger.warning("Api:[%s] Name:[%s] Result:[%s]" % (_hostgroup['api'], hostgroup_name, _hostgroup['status']))
    return jsonify(_hostgroup)


@app.route('/api/v1.0/maintenance/maintenance_status', methods=['POST'])
def maintenance_status():
    if not request.json or 'host_ip' not in request.json:
        abort(405)
    host_ip = request.json['host_ip']
    _maintenance = maintenance.maintenance_status(host_ip)
    if _maintenance['status']:
        api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_maintenance['api'], host_ip, _maintenance['status']))
    else:
        api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_maintenance['api'], host_ip, _maintenance['status']))
    return jsonify(_maintenance)


@app.route('/api/v1.0/maintenance/maintenance_create', methods=['POST'])
def maintenance_create():
    if not request.json or 'host_ip' not in request.json or 'start_time' not in request.json or 'end_time' not in request.json:
        abort(405)
    data = {}
    host_ip = request.json['host_ip']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    # start_time : 维护开始时间，固定格式：2018-02-06 13:14
    # end_time : 维护结束时间，固定格式：2018-02-06 19:14
    start_time = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M")))
    end_time = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M")))
    if (start_time < end_time) and (start_time > time.time()):
        _maintenance = maintenance.maintenance_create(host_ip, start_time, end_time)
        if _maintenance['status']:
            api_logger.info("Api:[%s] Ip:[%s] Result:[%s]" % (_maintenance['api'], host_ip, _maintenance['status']))
        else:
            api_logger.warning("Api:[%s] Ip:[%s] Result:[%s]" % (_maintenance['api'], host_ip, _maintenance['status']))
        return jsonify(_maintenance)
    else:
        data['result'] = "计划任务的时间设置错误！"
        data['status'] = False
        data['api'] = "根据ip修改对应监控主机的监控状态"
        return jsonify(data)

@app.route('/api/v1.0/action/is_autoregistration', methods=['POST'])
def is_autoregistration():
    if not request.json or 'autoregistration_name' not in request.json:
        abort(405)
    autoregistration_name = request.json['autoregistration_name']
    _autoregistration = action.is_autoregistration(autoregistration_name)
    if _autoregistration['status']:
        api_logger.info("Api:[%s] Name:[%s] Result:[%s]" % (_autoregistration['api'], autoregistration_name, _autoregistration['status']))
    else:
        api_logger.warning("Api:[%s] Name:[%s] Result:[%s]" % (_autoregistration['api'], autoregistration_name, _autoregistration['status']))
    return jsonify(_autoregistration)
