import requests
import json
import sys


class StashAPI:
    headers = {'ContentType': 'application/json'}

    def __init__(self, username="", password="", base_url=""):
        self.username = username
        self.password = password
        self.base_url = base_url

        if not (self.username and self.password and self.base_url):
            sys.exit("Missing config parameters for Stash API.")

        r = self._get("rest/api/1.0/projects")

        if(r.status_code != 200):
            sys.exit("Auth to Stash Unsuccessful. Exiting...")

    def _get(self, path):
        r = requests.get(self.base_url + path, headers=self.headers,
                         auth=(self.username, self.password))
        return r

    def get_repo(self, repo_name):
        projects = self.get_projects()

        for project in projects:
            repos = self.get_project_repos(project)
            for repo in repos:
                if repo == repo_name:
                    r = self._get("rest/api/1.0/projects/" +
                                  project + "/repos/" + repo)
                    return r.json()
        return None

    def get_projects(self):
        path = "rest/api/1.0/projects"
        qs = ""

        projects = []

        while True:
            r = self._get(path)

            for x in r.json()['values']:
                projects.append(x['key'])

            if r.json()['isLastPage'] == True:
                break
            else:
                qs = "?start=" + str(r.json()['start'] + r.json()['size'])

        return projects

    def get_project_repos(self, project):
        path = "rest/api/1.0/projects/" + project + "/repos"
        qs = ""

        repos = []

        while True:
            r = self._get(path + qs)

            for x in r.json()['values']:
                repos.append(x['slug'])

            if r.json()['isLastPage'] == True:
                break
            else:
                qs = "?start=" + str(r.json()['start'] + r.json()['size'])

        return repos

    def get_project_repo_pull_requests(self, project, repo):
        path = "rest/api/1.0/projects/" + \
            project + "/repos/" + repo + "/pull-requests?state=OPEN"
        qs = ""

        pull_requests = []

        while True:
            r = self._get(path + qs)

            for x in r.json()['values']:
                pull_requests.append(x)

            if r.json()['isLastPage'] == True:
                break
            else:
                qs = "&start=" + str(r.json()['start'] + r.json()['size'])

        return pull_requests

    def get_project_repo_pull_request_comments(
        self, project, repo, pull_request_id
    ):
        path = "rest/api/1.0/projects/" + \
            project + "/repos/" + repo + "/pull-requests/" + \
            str(pull_request_id) + "/activities"
        qs = ""

        comments = []

        while True:
            r = self._get(path + qs)

            for x in r.json()['values']:
                if (x['action'] == "COMMENTED"):
                    comments.append(x)

            if r.json()['isLastPage'] == True:
                break
            else:
                qs = "?start=" + str(r.json()['start'] + r.json()['size'])

        return comments
