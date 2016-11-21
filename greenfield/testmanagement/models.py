import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

@python_2_unicode_compatible
class TestSuite(models.Model):
    title = models.CharField(max_length=1024)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class TestCase(models.Model):
    title = models.CharField(max_length=1024)
    suite =  models.ForeignKey(TestSuite, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class TestRun(models.Model):
    title = models.CharField(max_length=1024)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

@python_2_unicode_compatible
class TestExecution(models.Model):
    STATUSES = ((0, 'UNEXECUTED'), (1, 'PASSED'), (2, 'FAILED'), (3, 'BLOCKED'))
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=0)
    run =  models.ForeignKey(TestRun, on_delete=models.CASCADE)
    case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  '%s: %s in %s' % (self.get_status_display(), self.case.title, self.run.title)

