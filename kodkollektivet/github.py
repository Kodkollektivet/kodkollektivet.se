import requests
from base64 import b64decode
import logging

from kodkollektivet.models import Project, Contributor, ProCon, ProLan, Language
from kodkollektivet.forms import ProjectForm

# If develop, use settings.settings, else
# use settings.production.
try:
    from settings.production import OAUTH_TOKEN
except ImportError:
    from settings.settings import OAUTH_TOKEN


log = logging.getLogger(__name__)


def getrepos():
    """
    This function collects all the repos from
    GitHub and store them in the database
    """
    req = requests.get('https://api.github.com/orgs/kodkollektivet/repos' + OAUTH_TOKEN)

    if req.status_code is not 200:
        log.warning(req.text)
        return

    projects = req.json()

    log.debug('Getting repos...')

    for project in projects:

        req = requests.get(
            'https://api.github.com/repos/kodkollektivet/' +
            project['name'] +
            '/readme' +
            OAUTH_TOKEN)

        if req.status_code is 200:
            try:
                readme = req.json()
                readme = b64decode(readme['content'])
            except Exception as e:
                log.debug(e)
        else:
            readme = ''

        form = ProjectForm({
            'gh_name': project['name'],
            'gh_id': project['id'],
            'gh_url': project['html_url'],
            'gh_readme': readme
        })

        if form.is_valid():
            # Creates or updates a project. It first looks it match on gh_name
            pro, created = Project.objects.update_or_create(
                gh_name=form.data['gh_name'],
                defaults=form.data)

            req = requests.get(
                'https://api.github.com/repos/kodkollektivet/' +
                project['name'] + '/languages' + OAUTH_TOKEN)

            if req.status_code is 200:
                languages = req.json()
                for key, value in languages.items():
                    lan, created = Language.objects.update_or_create(name=key)
                    obj, created = ProLan.objects.update_or_create(project=pro, language=lan)
            else:
                log.debug(req.text)
        else:
            log.warning('Form is not valid')
            log.warning(str(form.errors))


def getcontribs():
    """
    This function get all the project objects from the database.
    Ask the GitHub API for the contributors in the project.
    Save them to the database and create a relation.
    Project <-> Contributor
    """

    log.debug('Getting contributors...')

    for project in Project.objects.all():  # Get all projects

        # go in here if gh_name or gh_id
        if (len(project.gh_name) > 2) or (project.gh_id is not None):
            req = requests.get(
                'https://api.github.com/repos/kodkollektivet/' +
                project.gh_name +
                '/contributors' +
                OAUTH_TOKEN)

            if req.status_code is 200:
                for contributor in req.json():
                    import pdb; pdb.set_trace()
                    Contributor.objects.update_or_create(
                        gh_login=contributor['login'],
                        gh_url=contributor['url'],
                        gh_id=contributor['id'],
                        gh_html=contributor['html_url'],
                        gh_avatar=contributor['avatar_url'])
            else:
                log.debug(req.text)


def getprocon():
    """Get the project contributor relations."""

    log.debug('Getting procons...')

    for project in Project.objects.all():
        # If it is a github project
        if (len(project.gh_name) > 2) or (project.gh_id is not None):
            req = requests.get(
                'https://api.github.com/repos/kodkollektivet/' +
                project.gh_name +
                '/contributors' +
                OAUTH_TOKEN)

            if req.status_code is 200:
                for data in req.json():
                    contributor = Contributor.objects.get(gh_id=data['id'])
                    ProCon.objects.get_or_create(contributor=contributor, project=project)
            else:
                log.debug(req.status_code)
