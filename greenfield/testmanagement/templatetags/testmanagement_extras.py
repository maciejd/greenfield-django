from django import template
from testmanagement.models import TestRun, TestExecution
register = template.Library()

@register.filter(name='ratio')
def get_ratio(run_id, status):
    run = TestRun.objects.get(pk=run_id)
    all = TestExecution.objects.filter(run=run).count()
    selected = TestExecution.objects.filter(run=run, status=status).count()
    return selected/float(all)*100

@register.filter(name='label')
def get_label(status):
    map = {0:'default', 1:'success', 2:'danger',3:'warning'}
    return map[status]
