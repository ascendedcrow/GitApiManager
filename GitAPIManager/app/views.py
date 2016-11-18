"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import app.forms
from GitAPIManager.GitApiFunctions import CheckAndLogin
from django.shortcuts import redirect

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def issues(request):
    from GitAPIManager.GitApiFunctions import GitIssues
    from math import ceil
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    #Check User Login
    LoggedIn,GihubObject = CheckAndLogin(request)
    if (not LoggedIn):
        return login(request)

    page = request.GET.get('page')
    if (not page): page = 1
    issues,pages = GitIssues("WorkAtSwordfish/GitIntegration",GihubObject,page)
    return render(
        request,
        'app/issues.html',
        {
            'title':'Display Issues',
            'message':'All github issues displayed in a table.',
            'year':datetime.now().year,
            'issues':issues,
            'pages': range(pages)
        }
    )

def login(request):
    
    from GitAPIManager.GitApiFunctions import GitLogin


    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    form = app.forms.LoginForm(request.POST)

    if request.POST:
        if (form.is_valid()):
            try:
                if (not GitLogin(form.cleaned_data['username'],form.cleaned_data['password'])):
                    form.add_error("","Authentication Error")
                else:
                    request.session['username'] = form.cleaned_data['username']
                    request.session['loggedin'] = True
                    return home(request)
                    
            except Exception as e:
                form.add_error("","Authentication Error")
               
    return render(request,'app/login.html',
        {
            'form': form,
            'title': 'Log in',
            'year': datetime.now().year,
        }
    )


def createissue(request):
    from GitAPIManager.GitApiFunctions import SaveIssue
    

    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    form = app.forms.createissueform(request.POST)
    #Check User Login
    LoggedIn,GihubObject = CheckAndLogin(request)
    if (not LoggedIn):
        return login(request)

    if request.POST:
        if (form.is_valid()):
            if (SaveIssue(form.cleaned_data['title'],form.cleaned_data['description'],form.cleaned_data['assignto'],form.cleaned_data['client'],form.cleaned_data['priority'],
                          form.cleaned_data['category'],GihubObject,"WorkAtSwordfish/GitIntegration")):
                return home(request);
            else:
                form.add_error("","Errors is true")
    return render(request,'app/createissue.html',
        {
            'form': form,
            'title': 'Create Issue',
            'year': datetime.now().year,
        }
    )

