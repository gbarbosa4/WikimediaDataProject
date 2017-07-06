#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
from WDLG.views import write_galaxy_ip

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line

    galaxy_ip = sys.argv.pop(1)
    write_galaxy_ip(galaxy_ip)

    execute_from_command_line(sys.argv)
