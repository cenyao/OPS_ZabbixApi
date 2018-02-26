#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

loglevel = 'info'
bind = '127.0.0.1:5000'
pidfile = '/tmp/gunicorn.pid'
accesslog = '/data/log/zabbix_log/gunicorn-access.log'
errorlog = '/data/log/zabbix_log/gunicorn-error.log'
timeout = 30
backlog = 2048

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'