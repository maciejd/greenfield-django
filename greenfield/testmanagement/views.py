from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import TestRun,TestSuite,TestCase,TestExecution

class SuiteListView(generic.ListView):
    model = TestSuite
    template_name = 'testmanagement/suite_list.html'

class SuiteDetailView(generic.DetailView):
    model = TestSuite
    template_name = 'testmanagement/suite_detail.html'

@login_required
def add_suite(request):
    TestSuite(title=request.POST['title']).save()
    return HttpResponseRedirect(reverse('greenfield:suites'))
@login_required
def delete_suite(request, suite_id):
    get_object_or_404(TestSuite, pk=suite_id).delete()
    return HttpResponseRedirect(reverse('greenfield:suites'))
@login_required
def add_case(request, suite_id):
    ts = get_object_or_404(TestSuite, pk=suite_id)
    TestCase(title=request.POST['title'], suite=ts).save()
    return HttpResponseRedirect(reverse('greenfield:suite', kwargs={'pk':suite_id}))

@login_required
def delete_case(request, suite_id, case_id):
    get_object_or_404(TestCase, pk=case_id).delete()
    return HttpResponseRedirect(reverse('greenfield:suite', kwargs={'pk':suite_id}))

@login_required
def show_runs(request):
    runs = TestRun.objects.all()
    suites = TestSuite.objects.exclude(testcase__isnull=True)
    return render(request, 'testmanagement/run_list.html', {'runs': runs, 'suites': suites})

@login_required
def add_run(request):
    ts = get_object_or_404(TestSuite, pk=request.POST['suite_id'])
    tr = TestRun(title=request.POST['title'], suite=ts)
    tr.save()
    for tc in ts.testcase_set.all():
        TestExecution(case=tc, run=tr, status=0).save()
    return HttpResponseRedirect(reverse('greenfield:runs'))

@login_required
def delete_run(request, run_id):
    get_object_or_404(TestRun, pk=run_id).delete()
    return HttpResponseRedirect(reverse('greenfield:runs'))

@login_required
def show_run(request, run_id):
    tr = get_object_or_404(TestRun, pk=run_id)
    return render(request, 'testmanagement/run_detail.html', {'run': tr, 'STATUSES':TestExecution.STATUSES})

@login_required
def update_result(request, run_id, execution_id):
    e = get_object_or_404(TestExecution, pk=execution_id)
    e.status=request.POST['status']
    e.save()
    return HttpResponseRedirect(reverse('greenfield:run', kwargs={'run_id':run_id}))

class CaseDetailView(generic.DetailView):
    model = TestCase
    template_name = 'testmanagement/case_detail.html'
