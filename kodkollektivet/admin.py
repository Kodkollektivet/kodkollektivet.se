from django.contrib import admin

from . import models


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.BoardMember)
admin.site.register(models.Project, ProjectAdmin)
