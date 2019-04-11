#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    profile = os.environ.get('DJANGO_PROFILE', 'base')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblogs.settings.%s" % profile)
    print('************DJANGO_SETTINGS_MODULE======='
          +os.environ.get('DJANGO_SETTINGS_MODULE', 'DJANGO_SETTINGS_MODULE没有设置'))

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
