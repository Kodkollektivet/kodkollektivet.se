import requests
from base64 import b64decode
import logging

from kodkollektivet.models import Project

# If develop, use settings.settings, else
# use settings.production.
try:
    from settings.production import OAUTH_TOKEN
except ImportError:
    from settings.settings import OAUTH_TOKEN


log = logging.getLogger(__name__)


def _get_repo_data():
    req = requests.get('https://api.github.com/orgs/kodkollektivet/repos' + OAUTH_TOKEN)
    try:
        if req.status_code is 200:
            return [{'name': i['name'],
                     'stars': i['stargazers_count'],
                     'language': i['language'] if i['language'] else "",
                     'github_id': i['id'],
                     'github_url': i['url']
            } for i in req.json()]
        else:
            log.debug('Could not get repos from GitHub.')
            log.debug(req.text)
            return None

    except Exception as e:
        log.debug(e)
        return None


def _save_repos():
    try:
        repos = _get_repo_data()
        if repos:
            for repo in repos:
                Project.objects.update_or_create(github_id=repo['github_id'], defaults=repo)
    except Exception as e:
        log.debug(e)


def collect_github_data():
    _save_repos()
