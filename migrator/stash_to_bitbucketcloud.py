import requests
import json
import sys


class StashToBitBucketCloudMigrator:

    def __init__(self, stash_api=None, bitbucketcloud_api=None):
        self._stash_api = stash_api
        self._bitbucketcloud_api = bitbucketcloud_api
        self.stash_repo = None
        self.bitbucketcloud_repo = None

    def migrate(self, stash_repo, bitbucketcloud_repo):
        # 1. Check if PR exists in Stash and Bitbucket Cloud
        self.stash_repo = self._stash_preflight(stash_repo)
        self.bitbucketcloud_repo = self._bitbucketcloud_preflight(
            bitbucketcloud_repo)

        # 2. Iterate Stash PRs and Create PR if DNE
        stash_pull_requests = self._stash_api.get_project_repo_pull_requests(
            self.stash_repo['project']['key'], self.stash_repo['slug'])

        for pull_request in stash_pull_requests:
            # Check if PR exists in BitBucket
            bitbucket_pr = self._create_bitbucketcloud_pr_from_stash_pr(
                stash_pr=pull_request)

            if not bitbucket_pr:
                sys.exit("Problem creating pull request.")

            # 3. Grab Comments from Stash
            stash_comments = \
                self._stash_api.get_project_repo_pull_request_comments(
                    self.stash_repo['project']['key'],
                    self.stash_repo['slug'],
                    pull_request['id'])

            # 4. Insert Comments into Bitbucket Cloud
            for comment in stash_comments[::-1]:
                # print(json.dumps(comment, indent=4))
                bitbucket_comment = \
                    self._create_comment_from_stash_pr_comment(
                        bitbucket_pr,
                        comment)

                if not bitbucket_comment:
                    sys.exit("Problem creating comment.")

        return

    def _stash_preflight(self, stash_repo):
        repo = self._stash_api.get_repo(stash_repo)

        if not repo:
            sys.exit("Stash Preflight -- Repo: " +
                     stash_repo + " does not exist.")

        return repo

    def _bitbucketcloud_preflight(self, bitbucketcloud_repo):
        repo = self._bitbucketcloud_api.get_repo(bitbucketcloud_repo)

        if not repo:
            sys.exit("Bitbucket Cloud Preflight -- Repo: " +
                     bitbucketcloud_repo + " does not exist.")

        return repo

    def _create_bitbucketcloud_pr_from_stash_pr(self, stash_pr=None):
        bitbucketcloud_payload = {
            'username': self.bitbucketcloud_repo['owner']['username'],
            'repo': self.bitbucketcloud_repo['name'],
            'title': stash_pr['title'],
            'state': stash_pr['state'],
            'summary': {
                'raw': stash_pr['description']
            },
            'source': {
                'branch': {
                    'name': stash_pr['fromRef']['displayId']
                }
            },
            'destination': {
                'branch': {
                    'name': stash_pr['toRef']['displayId']
                }
            }
        }

        return self._bitbucketcloud_api.create_pullrequest(
            bitbucketcloud_payload)

    def _create_comment_from_stash_pr_comment(
            self, pull_request, stash_pr_comment=None):
        bitbucketcloud_payload = {
            'content': {
                'raw': stash_pr_comment['comment']['text']
            }
        }

        if 'commentAnchor' in stash_pr_comment.keys():
            line = 0
            if 'line' in stash_pr_comment['commentAnchor'].keys():
                line = stash_pr_comment['commentAnchor']['line']

            if stash_pr_comment['commentAnchor']['fileType'] == 'TO':
                bitbucketcloud_payload['inline'] = {
                    'to': line,
                    'path': stash_pr_comment['commentAnchor']['path']
                }
            else:
                bitbucketcloud_payload['inline'] = {
                    'from': line,
                    'path': stash_pr_comment['commentAnchor']['path']
                }

        return self._bitbucketcloud_api.create_pullrequest_comment(
            self.bitbucketcloud_repo,
            pull_request['id'],
            bitbucketcloud_payload)
