from django.contrib import admin
from .models import TestCase, TestRun, TestSuite, TestExecution


class CaseInline(admin.StackedInline):
    model = TestCase

class SuiteAdmin(admin.ModelAdmin):
    inlines = [CaseInline]

class ExecutionInline(admin.StackedInline):
    readonly_fields = ['updated_at']
    model = TestExecution

class RunAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']
    inlines = [ExecutionInline]

admin.site.register(TestSuite, SuiteAdmin)
admin.site.register(TestRun, RunAdmin)

