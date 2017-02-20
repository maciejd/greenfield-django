from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'greenfield'
urlpatterns = [
    url(r'^suite/$', login_required(views.SuiteListView.as_view()), name='suites'),
    url(r'^suite/(?P<pk>[0-9]+)/$', login_required(views.SuiteDetailView.as_view()), name='suite'),
    url(r'^suite/(?P<suite_id>[0-9]+)/add$', views.add_case, name='add_case'),
    url(r'^suite/(?P<suite_id>[0-9]+)/delete/(?P<case_id>[0-9]+)/$', views.delete_case, name='delete_case'),
    url(r'^suite/add$', views.add_suite, name='add_suite'),
    url(r'^suite/delete/(?P<suite_id>[0-9]+)/$', views.delete_suite, name='delete_suite'),
    url(r'^run/$', views.show_runs, name='runs'),
    url(r'^run/(?P<run_id>[0-9]+)/update/(?P<execution_id>[0-9]+)/$', views.update_result, name='update_result'),
    url(r'^run/(?P<run_id>[0-9]+)/', views.show_run, name='run'),
    url(r'^run/add$', views.add_run, name='add_run'),
    url(r'^run/delete/(?P<run_id>[0-9]+)/&$', views.delete_run, name='delete_run'),
    url(r'case/(?P<pk>[0-9]+)/$', login_required(views.CaseDetailView.as_view()), name='case'),
    url(r'^login/$', auth_views.login,  {'template_name': 'testmanagement/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'greenfield:login'}, name='logout'),
    url(r'^case/(?P<case_id>[0-9]+)/save$', views.save_case, name='save_case'),
    ]
