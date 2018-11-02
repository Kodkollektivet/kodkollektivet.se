# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def handle_uploaded_file(fname, f):
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class BoardMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='board-images/')

    def save(self, *args, **kwargs):
        super(BoardMember, self).save(*args, **kwargs)
        if self.photo:
            with Image(filename=self.photo.path) as img:
                img.save(filename=self.photo.path+'.ORGINAL')
                img.transform(resize='x250')
                img.compression_quality = 90
                img.save(filename=self.photo.path)
        if self.email:
            with Drawing() as draw:
                with Image(width=300,
                           height=30,
                           background=Color('white')) as emailimg:

                    draw.font = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
                    draw.font_color = 'black'
                    draw.font_size = 16
                    draw.text(5, int(emailimg.height * 12 / 13), self.email)

                    draw.draw(emailimg)
                    emailimg.save(filename=os.path.dirname(self.photo.path) +'/' + self.last_name + '.email.png')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Event(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Markdown syntax can be used!")
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    date = models.DateField()
    time = models.TimeField()
    publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    #objects = PostQuerySet.as_manager()

    def is_upcomming_event(self):
        return self.datetime >= timezone.now()

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Set slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event post"
        verbose_name_plural = "Event posts"
        ordering = ["-created_date"]


class Project(models.Model):
    name = models.CharField(max_length=254, unique=True)
    stars = models.IntegerField(default=0)
    language = models.CharField(max_length=254, default='')
    github_id = models.IntegerField(blank=True, null=True)
    github_url = models.CharField(max_length=254, blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        """Set slug"""
        if not self.name:
            self.name = self.gh_name
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.slug
