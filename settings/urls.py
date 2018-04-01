"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

from kodkollektivet import views

urlpatterns = i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.IndexView.as_view(), name='home'),
    re_path(r'^', include(('kodkollektivet.urls', 'kodkollektivet'), namespace='kodkollektivet')),
    # re_path(r'^i18n/', include('django.conf.urls.i18n')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
