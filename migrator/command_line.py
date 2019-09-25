import argparse
import sys
import os
from migrator.stash import StashAPI
from migrator.bitbucketcloud import BitBucketCloudAPI
from migrator.stash_to_bitbucketcloud import StashToBitBucketCloudMigrator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stash_repo', help='command help')
    parser.add_argument('bitbucketcloud_repo', help='command help')
    parser.add_argument('--stash-username',
                        default=os.environ.get('STASH_USERNAME', ''),
                        help='foo help')
    parser.add_argument('--stash-password',
                        default=os.environ.get('STASH_PASSWORD', ''),
                        help='foo help')
    parser.add_argument('--stash-base-url',
                        default=os.environ.get('STASH_BASE_URL', ''),
                        help='foo help')
    parser.add_argument('--bitbucketcloud-username',
                        default=os.environ.get('BITBUCKETCLOUD_USERNAME', ''),
                        help='foo help')
    parser.add_argument('--bitbucketcloud-password',
                        default=os.environ.get('BITBUCKETCLOUD_PASSWORD', ''),
                        help='foo help')
    parser.add_argument('--bitbucketcloud-base-url',
                        default=os.environ.get('BITBUCKETCLOUD_BASE_URL', ''),
                        help='foo help')
    args = parser.parse_args()

    print(args)

    #     if args.command == 'server':
    #         run_server()
    #     elif args.command == 'client':
    #         run_client()
    #     else:
    #         sys.exit("Invalid command. Exiting...")

    stash_api = StashAPI(username=args.stash_username,
                         password=args.stash_password,
                         base_url=args.stash_base_url)
    bitbucket_cloud_api = BitBucketCloudAPI(
        username=args.bitbucketcloud_username,
        app_password=args.bitbucketcloud_password,
        base_url=args.bitbucketcloud_base_url)

    stash_to_bitbucket_migrator = StashToBitBucketCloudMigrator(
        stash_api, bitbucket_cloud_api)

    stash_to_bitbucket_migrator.migrate(
        args.stash_repo, args.bitbucketcloud_repo)


if __name__ == "__main__":
    main()
