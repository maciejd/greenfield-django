from django.conf.urls import url

from . import views

app_name = 'greenfield'
urlpatterns = [
    url(r'^suite/$', views.SuiteListView.as_view(), name='suites'),
    url(r'^suite/(?P<pk>[0-9]+)/$', views.SuiteDetailView.as_view(), name='suite')
]
