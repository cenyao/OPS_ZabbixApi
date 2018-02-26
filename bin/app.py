#!/usr/bin/env python3
# -*- encoding: utf8 -*-
import os
import sys
from conf import settings
from core import main

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)

if __name__ == '__main__':
    # main.app.run(debug=True, host=settings.FLASK_HOST)
    # from werkzeug.contrib.fixers import ProxyFix
    # main.app.wsgi_app = ProxyFix(main.app.wsgi_app)
    main.app.run()
