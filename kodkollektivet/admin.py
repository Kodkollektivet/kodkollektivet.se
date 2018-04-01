from django.contrib import admin

from . import models


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug', 'gh_name', 'gh_id', 'gh_url')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug', 'gh_login', 'gh_url', 'gh_id', 'gh_html', 'gh_avatar')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('role',)
    exclude = ('slug',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)


class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)


class ProFraAdmin(admin.ModelAdmin):
    list_display = ('project', 'framework',)


class ProConAdmin(admin.ModelAdmin):
    list_display = ('project', 'contributor',)


class ProLanAdmin(admin.ModelAdmin):
    list_display = ('project', 'language',)


class ProRolAdmin(admin.ModelAdmin):
    list_display = ('project', 'contributor', 'role',)


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.BoardMember)

admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.Contributor, ContributorAdmin)
admin.site.register(models.Framework, FrameworkAdmin)
admin.site.register(models.Role, RoleAdmin)

admin.site.register(models.ProCon, ProConAdmin)
admin.site.register(models.ProLan, ProLanAdmin)
admin.site.register(models.ProRol, ProRolAdmin)
admin.site.register(models.ProFra, ProFraAdmin)
