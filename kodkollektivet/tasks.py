from __future__ import absolute_import
import os
import re
import time
import logging

from django.conf import settings

from celery import Celery
from celery.schedules import crontab
from celery import shared_task

from kodkollektivet.github import collect_github_data


log = logging.getLogger(__name__)


@shared_task
def daily_update():
    collect_github_data()
