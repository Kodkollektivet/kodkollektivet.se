from django.views.generic import ListView, DetailView

from .models import Project


class ProjectsListView(ListView):
    model = Project
    template_name = 'kodkollektivet_projects/projects.html'


class ProjectsDetailView(DetailView):
    model = Project
    template_name = 'kodkollektivet_projects/projects_detail_view.html'



