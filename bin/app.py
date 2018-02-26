#!/usr/bin/env python
# -*- encoding: utf8 -*-
import os
import sys
from conf import settings
from core import main

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)

if __name__ == '__main__':
    main.app.run(debug=True, host=settings.FLASK_HOST)
    # main.app.run(host=settings.FLASK_HOST)
