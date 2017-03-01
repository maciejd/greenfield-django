from django.test import TestCase as DjangoTestCase
from testmanagement.models import TestSuite, TestCase, TestExecution, TestRun
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client


def isLoggedIn(self):
    self.client = Client()
    self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    self.client.login(username='john', password='johnpassword')


def add_suite():
    s = TestSuite.objects.create(title='TestSuite')
    return s


def add_case(suite):
    c = TestCase.objects.create(title='TestCase', suite=suite)
    return c


def add_run(suite):
    r = TestRun.objects.create(title='TestRun', suite=suite)
    return r


def add_execution(case, run):
    e = TestExecution.objects.create(case=case, run=run, status=0)
    return e


class TestRunMethodTest(DjangoTestCase):
    def test_run_to_string(self):
        s = add_suite()
        add_case(s)
        r = add_run(s)
        self.assertEqual(str(r), 'TestRun')


class TestSuiteMethodTest(DjangoTestCase):
    def test_suite_to_string(self):
        s = add_suite()
        self.assertEqual(str(s), 'TestSuite')


class TestCaseMethodTest(DjangoTestCase):
    def test_cases_assigned_to_suite(self):
        s = add_suite()
        c1 = add_case(s)
        c2 = add_case(s)
        self.assertEqual(list(s.testcase_set.all()), [c1, c2])

    def test_suite_assigned_to_case(self):
        s = add_suite()
        c1 = add_case(s)
        self.assertEqual(c1.suite, s)

    def test_case_to_string(self):
        s = add_suite()
        c = add_case(s)
        self.assertEqual(str(c), 'TestCase')


class TestCaseExecutionMethodTest(DjangoTestCase):
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

    def test_case_to_string(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        self.assertEqual(str(e), 'UNEXECUTED: TestCase in TestRun')


class RunListViewTests(DjangoTestCase):
    def test_suite_not_returned_if_0_cases(self):
        add_suite()
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:runs'))
        self.assertQuerysetEqual(response.context['suites'], [])

    def test_suite_returned_if_gt0_cases(self):
        s = add_suite()
        add_case(s)
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:runs'))
        self.assertEqual(list(response.context['suites']), [s])

    def test_create_run(self):
        s = add_suite()
        add_case(s)
        isLoggedIn(self)
        self.client.post(reverse('greenfield:add_run'), {'title': 'TestRun', 'suite_id': s.id})
        self.assertEqual(TestRun.objects.all().count(), 1)
        self.assertEqual(TestRun.objects.all().first().suite, s)

    def test_runs_returned(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        add_execution(c, r)
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:runs'))
        self.assertEqual(list(response.context['runs']), [r])

    def test_delete_run(self):
        s = add_suite()
        add_case(s)
        r = add_run(s)
        isLoggedIn(self)
        response = self.client.post(reverse('greenfield:delete_run', kwargs={'run_id': r.id}), follow=True)
        self.assertQuerysetEqual(response.context['runs'], [])


class RunDetailViewTest(DjangoTestCase):
    def test_status_change(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        isLoggedIn(self)
        self.client.post(reverse('greenfield:update_result', kwargs={'run_id': r.id, 'execution_id': e.id}),
                         {'status': 1})
        self.assertEqual(TestExecution.objects.get(pk=e.pk).status, 1)

    def test_executions_returned(self):
        s = add_suite()
        c = add_case(s)
        r = add_run(s)
        e = add_execution(c, r)
        isLoggedIn(self)
        response = self.client.post(reverse('greenfield:run', kwargs={'run_id': r.id}))
        self.assertEqual(list(response.context['run'].testexecution_set.all()), [e])


class SuiteListViewTest(DjangoTestCase):
    def test_suites_returned(self):
        s = add_suite()
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:suites'))
        self.assertEqual(list(response.context['object_list']), [s])

    def test_add_suite(self):
        isLoggedIn(self)
        self.client.post(reverse('greenfield:add_suite'), {'title': 'TestSuite'})
        self.assertEqual(TestSuite.objects.all().count(), 1)
        self.assertEqual(TestSuite.objects.all().first().title, 'TestSuite')

    def test_remove_suite(self):
        s = add_suite()
        isLoggedIn(self)
        response = self.client.post(reverse('greenfield:delete_suite', kwargs={'suite_id': s.id}), follow=True)
        self.assertQuerysetEqual(response.context['object_list'], [])


class SuiteDetailViewTest(DjangoTestCase):
    def test_cases_displayed(self):
        s = add_suite()
        c1 = add_case(s)
        c2 = add_case(s)
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:suite', kwargs={'pk': s.id}))
        self.assertEqual(list(response.context['object'].testcase_set.all()), [c1, c2])

    def test_add_case(self):
        s = add_suite()
        isLoggedIn(self)
        self.client.post(reverse('greenfield:add_case', kwargs={'suite_id': s.id}), {'title': 'TestCase'})
        self.assertEqual(TestCase.objects.first().title, 'TestCase')
        self.assertEqual(s.testcase_set.first().title, 'TestCase')

    def test_remove_case(self):
        s = add_suite()
        c = add_case(s)
        isLoggedIn(self)
        response = self.client.post(reverse('greenfield:delete_case', kwargs={'suite_id': s.id, 'case_id': c.id}),
                                    follow=True)
        self.assertQuerysetEqual(response.context['object'].testcase_set.all(), [])


class CaseDetailViewTest(DjangoTestCase):
    def test_executions_displayed(self):
        s = add_suite()
        c = add_case(s)
        r1 = add_run(s)
        e1 = add_execution(c, r1)
        r2 = add_run(s)
        e2 = add_execution(c, r2)
        isLoggedIn(self)
        response = self.client.get(reverse('greenfield:case', kwargs={'pk': c.id}))
        self.assertEqual(list(response.context['object'].testexecution_set.all()), [e1, e2])

    def test_edit_case(self):
        s = add_suite()
        c = add_case(s)
        isLoggedIn(self)
        self.client.post(reverse('greenfield:save_case', kwargs={'case_id': c.id}), {'title': 'New Title'})
        c.refresh_from_db()
        self.assertEqual(c.title, 'New Title')
