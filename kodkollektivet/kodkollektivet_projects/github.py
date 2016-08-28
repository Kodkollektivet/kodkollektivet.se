import requests
from base64 import b64decode
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from kodkollektivet_projects.models import Project, Contributor, ProCon, ProLan, Language
from kodkollektivet_projects.forms import ProjectForm

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
    projects = requests.get('https://api.github.com/orgs/kodkollektivet/repos' + OAUTH_TOKEN).json()

    log.debug('Getting repos...')

    for project in projects:

        readme = requests.get(
            'https://api.github.com/repos/kodkollektivet/' + project['name'] + '/readme' + OAUTH_TOKEN).json()

        try:
            readme = b64decode(readme['content'])
        except:
            readme = ''

        form = ProjectForm({
            'gh_name': project['name'],
            'gh_id': project['id'],
            'gh_url': project['html_url'],
            'gh_readme': readme
        })

        if form.is_valid():
            # Creates or updates a project. It fist looks it match on gh_name
            pro, created = Project.objects.update_or_create(gh_name=form.data['gh_name'], defaults=form.data)

            languages = requests.get('https://api.github.com/repos/kodkollektivet/'+project['name']+'/languages' + OAUTH_TOKEN).json()

            for key, value in languages.items():
                lan, created = Language.objects.update_or_create(name=key)
                obj, created = ProLan.objects.update_or_create(project=pro, language=lan)

        else:
            log.debug('Form is not valid')
            log.debug(str(form.errors))


def getcontribs():
    """
    This function get all the project objects from the database.
    Ask the GitHub API for the contributors in the project.
    Save them to the database and create a relation.
    Project <-> Contributor
    """

    projects = Project.objects.all()  # Get all projects

    for project in projects:  # iterate over them

        if (len(project.gh_name) > 2) or (project.gh_id is not None):  # go in here if gh_name or gh_id

            request = requests.get('https://api.github.com/repos/kodkollektivet/'+project.gh_name+'/contributors' + OAUTH_TOKEN).json()

            for data in request:
                Contributor.objects.update_or_create(
                    gh_login=data['login'],
                    gh_url=data['url'],
                    gh_id=data['id'],
                    gh_html=data['html_url'],
                    gh_avatar=data['avatar_url']
                )


def getprocon():

    projects = Project.objects.all()

    for project in projects:

        if (len(project.gh_name) > 2) or (project.gh_id is not None):  # If it is a github project
            request = requests.get('https://api.github.com/repos/kodkollektivet/'+project.gh_name+'/contributors' + OAUTH_TOKEN).json()

            for data in request:
                contributor = Contributor.objects.get(gh_id=data['id'])
                ProCon.objects.get_or_create(contributor=contributor, project=project)


class GithubHook(APIView):

    permission_classes = (AllowAny,)

    def post(self, *args):
        getrepos()
        getcontribs()
        getprocon()
        return Response(status=status.HTTP_200_OK)