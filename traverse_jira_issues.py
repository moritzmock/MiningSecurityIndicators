import os
from dotenv import load_dotenv
from jira import JIRA
from tqdm import tqdm
from pprint import pprint
import pandas as pd
from utils import parser

load_dotenv()

TOKEN_JIRA = os.getenv('TOKEN_JIRA')

jira = JIRA(basic_auth=('moritz.mock.ext@wuerth-phoenix.net', TOKEN_JIRA),
            options={'server': 'https://siwuerthphoenix.atlassian.net'})


def get_all_issues(jira_client, project_name):
    issues = []

    i = 0

    chunk_size = 30

    pbar = tqdm(desc='Downloading chunks of issues...')

    while True:
        chunk = jira_client.search_issues(f'project = {project_name}', startAt=i, maxResults=chunk_size, json_result=True)
        i += chunk_size
        issues.append(chunk)
        pbar.update(chunk_size)

        if i >= chunk['total']:
            break

    pbar.close()
    return issues

if __name__ == '__main__':

    args = parser()

    all_issues = get_all_issues(jira, args.JIRA_PROJECT)

    df = pd.DataFrame(columns=['key_value', 'title', 'description', 'created', 'timespent', 'resolution', 'statuscategorychangedate', 'status_name', 'issue_type'])

    pbar = tqdm(total=len(all_issues), desc='Iterating through chunk of issues...')

    for issues in all_issues:

        pbar_2 = tqdm(total=len(issues), desc='Iterating through issues...', leave=False)

        for issue in issues['issues']:
            title = issue['fields']['summary'] # title
            description = issue['fields']['description'] # description
            created = issue['fields']['created'] # created
            timespent = issue['fields']['timespent'] # time spent
            resolution = 'not available' if issue['fields']['resolution'] is None else issue['fields']['resolution']['name'] # time spent
            statuscategorychangedate = issue['fields']['statuscategorychangedate'] # time spent
            status_name = issue['fields']['status']['name'] # time spent
            issue_type = issue['fields']['issuetype']['name'] # issue type
            key = issue['key']

            new_row = {
                'key_value': key,
                'title': title,
                'description': description,
                'created': created,
                'timespent': timespent,
                'resolution': resolution,
                'statuscategorychangedate': statuscategorychangedate,
                'status_name': status_name,
                'issue_type': issue_type
            }

            df.loc[len(df)] = new_row

            pbar_2.update(1)

        pbar_2.close()
        pbar.update(1)

    pbar.close()

    df.to_csv("{}/{}_jira.csv".format(args.path_logs, args.path), index=False)