from datetime import datetime, timedelta, time

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from django.views.generic.base import ContextMixin

from . import models


class FooterView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(FooterView, self).get_context_data(**kwargs)
        context['upcoming_events'] = models.Event.objects.filter(date__gte=datetime.now())
        context['next_event'] = context['upcoming_events'].first
        context['old_events'] = models.Event.objects.all().order_by('date')
        context['projects'] = models.Project.objects.all()[:3]
        return context
    

class IndexView(FooterView, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['header_text'] = 'Kodkollektivet'
        context['focused_projects'] = models.Project.objects.filter(in_focus=1)
        return context


class BoardTemplateView(FooterView, TemplateView):
    template_name = 'board.html'

    def get_context_data(self, **kwargs):
        context = super(BoardTemplateView, self).get_context_data(**kwargs)
        context['header_text'] = _('Board')
        return context
    

class EventsListView(FooterView, ListView):
    queryset = models.Event.objects.all()
    template_name = "events/events_list_view.html"

    def get_context_data(self, **kwargs):
        context = super(EventsListView, self).get_context_data(**kwargs)
        context['header_text'] = _('Events')
        return context


class EventsDetailView(FooterView, DetailView):
    model = models.Event
    template_name = "events/events_detail_view.html"


class ProjectsListView(FooterView, ListView):
    """Project List View"""
    model = models.Project
    template_name = 'projects/projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsListView, self).get_context_data(**kwargs)
        context['header_text'] = _('Projects')
        return context


class ProjectsDetailView(FooterView, DetailView):
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


class ContributorDetailView(FooterView, DetailView):
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
    
