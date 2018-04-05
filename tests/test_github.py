from unittest import skip
from django.test import TestCase, Client
from django.urls import resolve

from kodkollektivet.models import Project


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
