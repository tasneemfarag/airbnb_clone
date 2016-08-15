#!/usr/bin/python

from subprocess import call
from config import *

call(["uwsgi", "--socket", "127.0.0.1:" + str(PORT), "--wsgi-file", "app.py", "--callable", "app", "--processes", "4", "--threads", "2", "--stats", "127.0.0.1:9191"])
