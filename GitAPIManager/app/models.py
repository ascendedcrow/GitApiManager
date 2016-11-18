"""
Definition of models.
"""

from django.db import models

# Create your models here.
class git_login(models.Model):
    login_name  = models.CharField(max_length=100,primary_key = True) 
    password    = models.CharField(max_length=128)
    loggedin    = models.BooleanField()


class IssueObject(object):
    from github import Issue
    data = Issue,
    client = '',
    priority = '',
    category = '',
    issue_comments = ""