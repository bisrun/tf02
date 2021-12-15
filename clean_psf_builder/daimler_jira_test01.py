from jira import JIRA
import re

options = {"server": "http://192.168.11.44:8080"}
#jira = JIRA(options)
jira = JIRA(options, basic_auth=('flywhale', '1'))
# Get all projects viewable by anonymous users.
projects = jira.projects()
"""
issues_in_proj = jira.search_issues('project = AS2019BNZDOS AND issuetype = Task AND status in'
                                    ' (등록, 등록접수, 해결진행중, 결과확인중) AND "이슈 구분" = 외부이슈 '
                                    'ORDER BY summary ASC', maxResults=None)
                                   
"""


issues_in_proj = jira.search_issues('project = AS2019BNZDOS AND issuetype = Task AND "이슈 구분" = 외부이슈 '
                                    'ORDER BY summary ASC' )
#print(issues_in_proj)
p =re.compile(r"""^<Analysis Result>\s*\w+.*\s*<""", re.MULTILINE)

for issue in issues_in_proj:
    print('{}: {}'.format(issue.key, issue.fields.summary))
    issuecmt = jira.issue(issue.key, expand='comments')
    for comment in issuecmt.fields.comment.comments:
        print("Comment: %s, %s, %s, %s" % (comment.id, comment.created, comment.author, comment.body))
        m=p.findall(comment.body)
        print(m)

print("-end-")