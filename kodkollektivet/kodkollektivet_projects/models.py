from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=254, unique=True)
    slug = models.SlugField(blank=True)

    # Github specific
    gh_name = models.CharField(max_length=254, blank=True)
    gh_id = models.IntegerField(blank=True, null=True)
    gh_url = models.CharField(max_length=254, blank=True)
    gh_readme = models.TextField(blank=True, help_text='Project readme. Markdown syntax!')

    def save(self, *args, **kwargs):

        """
        Set slug
        """
        if not self.name:
            self.name = self.gh_name

        if not self.slug:
            self.slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return self.slug


class Role(models.Model):
    role = models.CharField(max_length=254, blank=True)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = slugify(self.role)
        super(Role, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug


class Contributor(models.Model):
    name = models.CharField(max_length=254, blank=True)
    slug = models.CharField(max_length=254, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.CharField(max_length=254, blank=True)
    linkedin = models.CharField(max_length=254, blank=True)
    about = models.TextField(blank=True, help_text='Markdown syntax')

    # Github specific
    gh_login = models.CharField(max_length=254)
    gh_url = models.CharField(max_length=254)
    gh_id = models.IntegerField()
    gh_html = models.CharField(max_length=254, blank=True)
    gh_avatar = models.CharField(max_length=254, blank=True)

    class Meta:
        ordering = ['slug']

    def save(self, *args, **kwargs):
        """
        Set name and slug
        """
        if not self.name:
            self.name = self.gh_login
            self.slug = slugify(self.gh_login)

        super(Contributor, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug


class Language(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = self.name
        super(Language, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug


class Framework(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=254, blank=True)

    def save(self, *args, **kwargs):
        """
        Set slug
        """
        self.slug = self.name
        super(Framework, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug


class ProFra(models.Model):
    project = models.ForeignKey(Project)
    framework = models.ForeignKey(Framework)

    class Meta:
        verbose_name = 'Project-Framework relation'


class ProCon(models.Model):
    project = models.ForeignKey(Project)
    contributor = models.ForeignKey(Contributor)

    class Meta:
        verbose_name = 'Project-Contributor relation'


class ProLan(models.Model):
    project = models.ForeignKey(Project)
    language = models.ForeignKey(Language)

    class Meta:
        verbose_name = 'Project-Language relation'


class ProRol(models.Model):
    project = models.ForeignKey(Project)
    contributor = models.ForeignKey(Contributor)
    role = models.ForeignKey(Role)

    class Meta:
        verbose_name = 'Project-Role-Contributor relation'
