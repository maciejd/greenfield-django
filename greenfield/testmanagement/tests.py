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

class TestCaseExecutionMethodTest(TestCase):
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

    def test_runs_returned(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        response = self.client.get(reverse('greenfield:runs'))
        self.assertEqual(list(response.context['runs']),[r])

    def test_delete_run(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        response = self.client.post(reverse('greenfield:delete_run', kwargs={'run_id': r.id}), follow=True)
        self.assertQuerysetEqual(response.context['runs'], [])


class RunDetailViewTest(TestCase):
    def test_status_change(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        response = self.client.post(reverse('greenfield:update_result', kwargs={'run_id': r.id, 'execution_id': e.id}), {'status':1})
        self.assertEqual(models.TestExecution.objects.get(pk=e.pk).status, 1)

    def test_executions_returned(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        response = self.client.post(reverse('greenfield:run', kwargs={'run_id': r.id}))
        self.assertEqual(list(response.context['run'].testexecution_set.all()), [e])

class SuiteListViewTest(TestCase):
    def test_suites_returned(self):
        s = add_suite()
        response = self.client.get(reverse('greenfield:suites'))
        self.assertEqual(list(response.context['object_list']), [s])

    def test_add_suite(self):
        response = self.client.post(reverse('greenfield:add_suite'), {'title': 'TestSuite'})
        self.assertEqual(models.TestSuite.objects.all().count(), 1)
        self.assertEqual(models.TestSuite.objects.all().first().title, 'TestSuite')

    def test_remove_suite(self):
        s = add_suite()
        response = self.client.post(reverse('greenfield:delete_suite', kwargs={'suite_id': s.id}), follow=True)
        self.assertQuerysetEqual(response.context['object_list'], [])
    
class SuiteDetailViewTest(TestCase):
    def test_cases_displayed(self):
        s = add_suite()
        c1 = add_case(s)
        c2 = add_case(s)  
        response = self.client.get(reverse('greenfield:suite', kwargs={'pk': s.id}))
        self.assertEqual(list(response.context['object'].testcase_set.all()), [c1, c2])

    def test_add_case(self):
        s = add_suite()
        response = self.client.post(reverse('greenfield:add_case', kwargs={'suite_id': s.id}), {'title': 'TestCase'})
        self.assertEqual(models.TestCase.objects.first().title, 'TestCase')
        self.assertEqual(s.testcase_set.first().title, 'TestCase')

    def test_remove_case(self):
        s = add_suite()
        c = add_case(s)
        response = self.client.post(reverse('greenfield:delete_case', kwargs={'suite_id': s.id, 'case_id': c.id}), follow=True)
        self.assertQuerysetEqual(response.context['object'].testcase_set.all(), [])
        
class CaseDetailViewTest(TestCase):
    def test_executions_displayed(self):
        s = add_suite()
        c = add_case(s)
        r1 = add_run(s)
        e1 = add_execution(c, r1)
        r2 = add_run(s)
        e2 = add_execution(c, r2)
        response = self.client.get(reverse('greenfield:case', kwargs={'pk': c.id}))
        self.assertEqual(list(response.context['object'].testexecution_set.all()), [e1, e2])
