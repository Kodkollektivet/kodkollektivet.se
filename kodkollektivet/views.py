from datetime import datetime, timedelta, time

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from django.views.generic.base import ContextMixin

from . import models


class FooterView(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(FooterView, self).get_context_data(**kwargs)
        context['upcoming_events'] = models.Event.objects.filter(
            date__gte=datetime.now())
        context['next_event'] = context['upcoming_events'].first
        context['old_events'] = models.Event.objects.all().order_by('date')
        return context


class IndexView(FooterView, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['header_text'] = 'Kodkollektivet'
        return context


class BoardTemplateView(FooterView, ListView):
    template_name = 'board.html'
    queryset = models.BoardMember.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BoardTemplateView, self).get_context_data(**kwargs)
        context['header_text'] = _('Board')
        return context


class ThanksTemplateView(FooterView, TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(ThanksTemplateView, self).get_context_data(**kwargs)
        context['header_text'] = _('Thanks')
        return context


class EventsListView(FooterView, ListView):
    queryset = models.Event.objects.all().order_by('-date')
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
