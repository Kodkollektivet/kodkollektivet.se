from datetime import datetime, timedelta, time

from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone

from . import models


class IndexView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        m = models.Event.objects.filter(date__gte=datetime.now())
        context['upcomming_events'] = m
        return context
    

class EventsListView(ListView):
    queryset = models.Event.objects.all()
    template_name = "events/events_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(EventsListView, self).get_context_data(**kwargs)
        context['header_text'] = 'Events'
        return context


class EventsDetailView(DetailView):
    model = models.Event
    template_name = "events/events_detail_view.html"


class ProjectsListView(ListView):
    """Project List View"""
    model = models.Project
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsListView, self).get_context_data(**kwargs)
        context['header_text'] = 'Projects'
        return context


class ProjectsDetailView(DetailView):
    """Project Detail View"""
    model = models.Project
    template_name = 'projects/projects_detail_view.html'

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
    template_name = 'projects/contributor_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        procons = models.ProCon.objects.filter(contributor__gh_id=gh_id)
        projects = [i.project for i in procons]
        context['projects'] = projects
        return context
    
