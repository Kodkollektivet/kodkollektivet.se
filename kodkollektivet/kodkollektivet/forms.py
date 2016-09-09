from django.forms import ModelForm

from .models import Project, Contributor


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('gh_name', 'gh_id', 'gh_url', 'gh_readme')


class ContributorForm(ModelForm):
    class Meta:
        model = Contributor
        fields = ('gh_login', 'gh_url', 'gh_id')