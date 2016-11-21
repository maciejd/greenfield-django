from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import TestRun,TestSuite,TestCase,TestExecution

def index(request):
    return HttpResponse("Welcome to Greenfield")

class SuiteListView(generic.ListView):
    model = TestSuite
    template_name = 'testmanagement/suite_list.html'

class SuiteDetailView(generic.DetailView):
    model = TestSuite
    template_name = 'testmanagement/suite_detail.html'
