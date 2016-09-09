from django.views.generic import TemplateView, ListView, DetailView

from . import models


class IndexView(TemplateView):
    template_name = 'core/core.html'


class ProjectsListView(ListView):
    """Project List View"""
    model = models.Project
    template_name = 'kodkollektivet_projects/projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsListView, self).get_context_data(**kwargs)
        context['header_text'] = 'Projects'
        return context


class ProjectsDetailView(DetailView):
    """Project Detail View"""
    model = models.Project
    template_name = 'kodkollektivet_projects/projects_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        procons = models.ProCon.objects.filter(project__gh_id=gh_id)
        profras = models.ProFra.objects.filter(project__gh_id=gh_id)
        prolans= models.ProLan.objects.filter(project__gh_id=gh_id)
        languages = [i.language for i in prolans]
        contributors = [i.contributor for i in procons]
        frameworks = [i.framework for i in profras]
        context['header_text'] = kwargs['object'].name
        context['languages'] = languages
        context['contributors'] = contributors
        context['frameworks'] = frameworks
        return context


class ContributorDetailView(DetailView):
    """Contributor Detail View"""
    model = models.Contributor
    template_name = 'kodkollektivet_projects/contributor_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        procons = models.ProCon.objects.filter(contributor__gh_id=gh_id)
        projects = [i.project for i in procons]
        context['projects'] = projects
        return context
    
