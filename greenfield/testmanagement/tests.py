from django.test import TestCase
import models
from django.urls import reverse
# Create your tests here.

def add_suite():
    s = models.TestSuite.objects.create(title='test')
    return s

def add_case(suite):
    c = models.TestCase.objects.create(title='test', suite=suite)
    return c

def add_run(suite):
    r = models.TestRun.objects.create(title='test', suite=suite)
    return r

def add_execution(case, run):
    e = models.TestExecution.objects.create(case=case, run=run, status=0)
    return e

class TestCaseMethodTest(TestCase):
    def test_cases_assigned_to_suite(self):
        s = add_suite()
        c1 = add_case(s)
        c2 = add_case(s)
        self.assertEqual(list(s.testcase_set.all()), [c1,c2])
    
    def test_suite_assigned_to_case(self):
        s = add_suite()
        c1 = add_case(s)
        self.assertEqual(c1.suite, s)

class TestCaseExecutionTest(TestCase):
    def test_executions_assigned_to_run(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        self.assertEqual(list(r.testexecution_set.all()), [e])
 
    def test_executions_assigned_to_case(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        self.assertEqual(list(c.testexecution_set.all()), [e])
    
    def test_run_assigned_to_execution(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        self.assertEqual(e.run, r)
    
    def test_case_assigned_to_execution(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        self.assertEqual(e.case, c)
      
class RunListViewTests(TestCase):
    def test_suite_not_returned_if_0_cases(self):
        s = add_suite()
        response = self.client.get(reverse('greenfield:runs'))
        self.assertQuerysetEqual(response.context['suites'],[])

    def test_suite_returned_if_gt0_cases(self):
        s = add_suite()
        c = add_case(s)
        response = self.client.get(reverse('greenfield:runs'))
        self.assertEqual(list(response.context['suites']), [s])
    
    def test_create_run(self):
        s = add_suite()
        c = add_case(s)
        response = self.client.post(reverse('greenfield:add_run'), {'title': 'TestRun', 'suite_id': s.id})
        self.assertEqual(models.TestRun.objects.all().count(), 1)
        self.assertEqual(models.TestRun.objects.all().first().suite, s)

class RunDetailViewTest(TestCase):
    def test_status_change(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        response = self.client.post(reverse('greenfield:update_result', kwargs={'run_id': r.id, 'execution_id': e.id}), {'status':1})
        self.assertEqual(models.TestExecution.objects.get(pk=e.pk).status, 1)
 

