#!/usr/bin/env python3
# -*- encoding: utf8 -*-

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

loglevel = 'info'
bind = '127.0.0.1:5000'
pidfile = 'logs/gunicorn.pid'
logfile = 'logs/debug.log'

#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'