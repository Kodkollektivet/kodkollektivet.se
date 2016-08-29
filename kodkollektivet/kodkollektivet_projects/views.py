from django.views.generic import ListView, DetailView

from .models import Project, Contributor, ProCon


class ProjectsListView(ListView):
    model = Project
    template_name = 'kodkollektivet_projects/projects.html'


class ProjectsDetailView(DetailView):
    model = Project
    template_name = 'kodkollektivet_projects/projects_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectsDetailView, self).get_context_data(**kwargs)
        gh_id = kwargs['object'].gh_id
        print(gh_id)
        procons = ProCon.objects.filter(project__gh_id=gh_id)
        for i in procons:
            print(i.project.gh_id)
        return context


