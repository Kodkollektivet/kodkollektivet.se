from django.conf.urls import url

from kodkollektivet_projects import github
from kodkollektivet_projects import views

urlpatterns = [
    url(r'^$', views.ProjectsListView.as_view(), name='projectslistview'),
    url(r'^contributor/(?P<slug>\S+)/$', views.ContributorDetailView.as_view(), name="contributordetailview"),
    url(r'^(?P<slug>\S+)/$', views.ProjectsDetailView.as_view(), name="projectdetailview"),
    url(r'^github/webhook$', github.GithubHook.as_view(), name='githubwebhook'),
]