import requests
import json
import sys


class BitBucketCloudAPI:
    headers = {'ContentType': 'application/json'}

    def __init__(self, username="", app_password="", base_url=""):
        self.username = username
        self.app_password = app_password
        self.base_url = base_url

        if not (self.username and self.app_password and self.base_url):
            sys.exit("Missing config parameters for BitBucket API.")

        r = self._get("2.0/repositories")

        if(r.status_code != 200):
            sys.exit("Auth to BitBucket Unsuccessful. Exiting...")

    def _get(self, path, qs=""):
        if qs:
            r = requests.get(self.base_url + path + "?" + qs,
                             headers=self.headers,
                             auth=(self.username, self.app_password))
        else:
            r = requests.get(self.base_url + path, headers=self.headers,
                             auth=(self.username, self.app_password))

        return r

    def _post(self, path, payload=None, qs=""):
        if qs:
            r = requests.post(self.base_url + path + "?" + qs,
                              json=payload,
                              headers=self.headers,
                              auth=(self.username, self.app_password))
        else:
            r = requests.post(self.base_url + path,
                              json=payload,
                              headers=self.headers,
                              auth=(self.username, self.app_password))

        return r

    def get_repo(self, repo_name):
        r = self._get("2.0/repositories/" + repo_name)

        if r.status_code == 200:
            return r.json()

        return None

    def create_pullrequest(self, payload):
        r = self._post("2.0/repositories/" + payload['username'] + "/"
                       + payload['repo'] + "/pullrequests/",
                       payload=payload)

        if r.status_code != 201:
            None

        return r.json()

    def create_pullrequest_comment(self, repo, pull_request_id, payload):
        r = self._post("2.0/repositories/" + repo['owner']['username'] + "/"
                       + repo['name'] + "/pullrequests/" +
                       str(pull_request_id) + "/comments",
                       payload=payload)

        if r.status_code != 201:
            return None

        return r.json()
