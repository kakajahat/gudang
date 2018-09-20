#!/usr/bin/env python3
#
# jangan lupa
# export FLASK_APP && FLASK_ENV

import os

from app import create_app

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)
