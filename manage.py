#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
            raise

    galaxy_ip = sys.argv.pop(1)

    f = open(os.path.dirname(os.path.abspath(__file__)) + '/galaxy_ip', 'w')
    f.write(galaxy_ip)
    f.close()

    execute_from_command_line(sys.argv)
