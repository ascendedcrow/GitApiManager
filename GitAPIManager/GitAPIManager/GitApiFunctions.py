from github import *


def CheckAndLogout(request):
    try:
        del request.session['username'] 
        del request.session['loggedin']  
    except KeyError:
        pass

def CheckAndLogin(request):
    from app.models import git_login
    gh = None
    try:
        #Check if logged in
        if not request.session.get('loggedin'):
            CheckAndLogout(request)
            return False,gh

        #user logged in, get name and select from db
        UserName = request.session.get('username')
        if (UserName!=''):
            gitlogin = git_login.objects.filter(login_name=UserName)
            try:
                if (gitlogin):
                    gh = Github(gitlogin[0].login_name ,gitlogin[0].password)
                    request.session['username'] = UserName
                    request.session['loggedin'] = True
                    return True,gh
            except Exception as e:
                #error on loging in
                CheckAndLogout(request)
                return False,None
    except KeyError:
        CheckAndLogout(request)
        return False,None
    CheckAndLogout(request)
    return False,None

def GitLoginOAuth (UserName,Password):
    from app.models import git_login
    auth = GitLoginOAuth(UserName,Password)

def GitLogin (UserName,Password):
    from app.models import git_login
    try:
        gh = Github(UserName,Password)
        if gh.get_user(UserName):
            gitLogin = git_login(login_name = UserName, password = Password,loggedin = True)
            gitLogin.save();
            return True
        else:
            return False
    except Exception as e:
        #TODO: 401 (Authentication Error for more precise error handling)
        return False

def GitIssues(repo,gh,page):
    from math import ceil
    from app.models import IssueObject
    ret_issue = []
    repoObject = gh.get_repo(repo)
    ## Pagenation
    ##check item to start
    itemInPage = 10
    startItem = ((page-1) * itemInPage) 
    c = 1;
    AllIssues = repoObject.get_issues()
    for issue in  AllIssues:
        
        if (startItem > c):
            continue
        if (c % (itemInPage + 2) == 0):
            break;
        getIssueDict = GetLabelFromIssue(issue)
        IssueO =  IssueObject();
        IssueO.data     = getIssueDict['data']
        if getIssueDict['client']:
            IssueO.client   = getIssueDict['client'][0].name 
        else:
            IssueO.client  = ""
        if getIssueDict['priority']:
            IssueO.priority = getIssueDict['priority'][0].name
        else:
            IssueO.priority = ""
        if getIssueDict['category']:
            IssueO.category = getIssueDict['category'][0].name
        else:
            IssueO.category = ""

        for comm in issue.get_comments():
            IssueO.issue_comments += comm.body + "\n"

        c+=1
        ret_issue.append(IssueO)

    ##Crappy githubs pagenation does not work so need to count it
    c2 = 0;
    for Issue in AllIssues:
        c2+=1;
    return ret_issue, ceil(c2/itemInPage)
    

def GetLabelFromIssue(issue):

    client      = filter(lambda x: x.name[0:2] == "C:", issue.labels)
    priority    = filter(lambda x: x.name[0:2] == "P:", issue.labels)
    category    = filter(lambda x: x.name[0:4] == "Cat:", issue.labels)

    return {
           'data'       : issue,
           'client'     : [item for item in client  ] ,
           'priority'   : [item for item in priority] ,
           'category'   : [item for item in category] ,
           }

def GetClientDropDown(repo):
    gh =Github("swordfishtest","warr10r")
    ret_issue = []
    repoObject = gh.get_repo("WorkAtSwordfish/GitIntegration")
    Repo_Labels = repoObject.get_labels()
    ret_obje = []
    c = 0
    for repo_label in Repo_Labels:
        if (repo_label.name[0:2] == "C:"):
            c+=1
            ret_obje.append((repo_label.name,repo_label.name))

    #ret_obje = tuple(ret_obje);
    return tuple(ret_obje)

def GetPriorityDropDown(repo):
    gh =Github("swordfishtest","warr10r")
    ret_issue = []
    repoObject = gh.get_repo("WorkAtSwordfish/GitIntegration")
    Repo_Labels = repoObject.get_labels()
    ret_obje = []
    c = 0
    for repo_label in Repo_Labels:
        if (repo_label.name[0:2] == "P:"):
            c+=1
            ret_obje.append((repo_label.name,repo_label.name))

    #ret_obje = tuple(ret_obje);
    return tuple(ret_obje)

def GetCategoryDropDown(repo):
    gh =Github("swordfishtest","warr10r")
    ret_issue = []
    repoObject = gh.get_repo("WorkAtSwordfish/GitIntegration")
    Repo_Labels = repoObject.get_labels()
    ret_obje = []
    c = 0
    for repo_label in Repo_Labels:
        if (repo_label.name[0:4] == "Cat:"):
            c+=1
            ret_obje.append((repo_label.name,repo_label.name))

    #ret_obje = tuple(ret_obje);
    return tuple(ret_obje)

def GetUserDropDown(repo):
    gh =Github("swordfishtest","warr10r")
    ret_issue = []
    repoObject = gh.get_repo("WorkAtSwordfish/GitIntegration")
    assignees = repoObject.get_assignees()
    ret_obje = []
    c = 0
    for assignee in assignees:
        c+=1
        ret_obje.append((assignee.login,assignee.login))

    #ret_obje = tuple(ret_obje);
    return tuple(ret_obje)

def SaveIssue(title,body,asignee,clientLabel,priorityLabel,categoryLabel,gh,repo):
    repoObject = gh.get_repo(repo)
    ListLabels = []
    ListLabels.append(repoObject.get_label(clientLabel))
    ListLabels.append(repoObject.get_label(priorityLabel))
    ListLabels.append(repoObject.get_label(categoryLabel))
    ListLabels.append(repoObject.get_label(clientLabel))
    repoObject.create_issue(title,body,assignee=asignee,labels=ListLabels)