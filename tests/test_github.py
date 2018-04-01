from unittest import skip
from django.test import TestCase, Client
from django.core.urlresolvers import resolve

from kodkollektivet.models import Project, Contributor


class TestProjectsEndpoint(TestCase):
    """Tests for project/github related functions."""
    def setUp(self):
        self.client = Client()

    def test_projects_url(self):
        req = self.client.get('/en/projects/')
        self.assertEqual(req.status_code, 200)

    def test_projects_view(self):
        route = resolve('/en/projects/')
        self.assertEqual(route.func.__name__, 'ProjectsListView')

    def test_projects_url_name(self):
        route = resolve('/en/projects/')
        self.assertEqual(route.url_name, 'projectslistview')

    def test_projects_view_name(self):
        route = resolve('/en/projects/')
        self.assertEqual(route.view_name, 'kodkollektivet:projectslistview')

    def test_projects_template(self):
        route = resolve('/en/projects/')
        self.assertEqual(route.func.view_class.template_name, 'projects/projects.html')

    def test_projects_model(self):
        route = resolve('/en/projects/')
        self.assertEqual(route.func.view_class.model.__name__, 'Project')


class TestSpecificProjectEndpoint(TestCase):
    """Tests for specific project endpoint."""
    def setUp(self):
        self.client = Client()
        self.project = Project(
            name='TestProject',
            in_focus=False,
        )
        self.project.save()

    def test_project_slug(self):
        self.assertEqual(self.project.slug, 'testproject')

    def test_project_url(self):
        """Test the url."""
        req = self.client.get('/en/project/testproject/')
        self.assertEqual(req.status_code, 200)

    def test_project_view(self):
        route = resolve('/en/project/testproject/')
        self.assertEqual(route.func.__name__, 'ProjectsDetailView')

    def test_project_url_name(self):
        route = resolve('/en/project/testproject/')
        self.assertEqual(route.url_name, 'projectdetailview')

    def test_project_view_name(self):
        route = resolve('/en/project/testproject/')
        self.assertEqual(route.view_name, 'kodkollektivet:projectdetailview')

    def test_project_template(self):
        route = resolve('/en/project/testproject/')
        self.assertEqual(route.func.view_class.template_name, 'projects/projects_detail_view.html')

    def test_project_model(self):
        route = resolve('/en/project/testproject/')
        self.assertEqual(route.func.view_class.model.__name__, 'Project')


class TestContributorEndpoint(TestCase):
    """Tests for specific project endpoint."""
    def setUp(self):
        self.client = Client()
        self.contributor = Contributor(
            gh_login='test-login',
            gh_url='test-url',
            gh_id=1,
        )
        self.contributor.save()

    def test_contributor_slug(self):
        self.assertEqual(self.contributor.slug, 'test-login')

    def test_contributor_url(self):
        """Test the url."""
        req = self.client.get('/en/contributor/test-login/')
        self.assertEqual(req.status_code, 200)

    def test_contributor_view(self):
        route = resolve('/en/contributor/test-login/')
        self.assertEqual(route.func.__name__, 'ContributorDetailView')

    def test_contributor_url_name(self):
        route = resolve('/en/contributor/test-login/')
        self.assertEqual(route.url_name, 'contributordetailview')

    def test_contributor_view_name(self):
        route = resolve('/en/contributor/test-login/')
        self.assertEqual(route.view_name, 'kodkollektivet:contributordetailview')

    def test_contributor_template(self):
        route = resolve('/en/contributor/test-login/')
        self.assertEqual(route.func.view_class.template_name,
                         'projects/contributor_detail_view.html')

    def test_contributor_model(self):
        route = resolve('/en/contributor/test-login/')
        self.assertEqual(route.func.view_class.model.__name__, 'Contributor')
