from django.conf.urls import url

from . import views

app_name = 'greenfield'
urlpatterns = [
    url(r'^suite/$', views.SuiteListView.as_view(), name='suites'),
    url(r'^suite/add_suite$', views.add_suite, name='add_suite'),
    url(r'^suite/delete_suite/(?P<pk>[0-9]+)/$', views.delete_suite, name='delete_suite'),
    url(r'^suite/(?P<pk>[0-9]+)/$', views.SuiteDetailView.as_view(), name='suite')
]
