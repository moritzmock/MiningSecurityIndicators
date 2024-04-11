import requests
from utils import parser
from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

TOKEN_GITHUB = os.getenv('TOKEN_GITHUB')

headers = {
    'Authorization': f'token {TOKEN_GITHUB}'
}

def fetch_data(data):
    return requests.get(data, headers=headers).json()


def parse_comment(data):
    if data is None:
        return ""
    comment_split = data.split('\n')
    result = []
    for line in comment_split:
        line_space_free = line.replace(" ", "")
        if line_space_free.startswith('>'):
            pass
        elif line_space_free.startswith('!['):
            pass
        else:
            result.append(line)

    return '\n'.join(result)


if __name__ == '__main__':

    args = parser()

    statuses = ['open', 'closed']

    pbar = tqdm(total=len(statuses), desc="Fetching data") # <open|closed>

    df = pd.DataFrame(columns=['title', 'issue_link', 'issue_desc', 'pull_request', 'number_comments', 'comments_link', 'comments',
                               'created_at', 'closed_at', 'status'])

    for status in statuses:

        pbar_page = tqdm(desc="Iterating pages...", leave=False)

        for page in range(1, 1000):

            url = "https://api.{}/issues?state={}&page={}".format(args.GITHUB, status, page)
            data = fetch_data(url)

            if(len(data) == 0):
                break

            if(len(data) < 5):
                pprint(data)


            pbar_page.update(1)

            for issue in data:
                title = issue['title']
                html_url = issue['html_url']
                number_comments = int(issue['comments'])
                comments_link = issue['comments_url']
                created_at = issue['created_at']
                closed_at = issue['closed_at']
                message = parse_comment(issue['body'])
                pull_request = True if 'pull_request' in issue.keys() else False

                comments = []

                comments = "\n$$\n".join(comments)

                new_row = {'title': title, 'issue_link': html_url, 'issue_desc': message, 'pull_request': pull_request,
                           'number_comments': number_comments, 'comments_link': comments_link, 'comments': comments,
                           'created_at': created_at, 'closed_at': closed_at, 'status': status}

                df.loc[len(df)] = new_row

        pbar_page.close()

        pbar.update(1)

    pbar.close()

    df.to_csv("{}/{}_github.csv".format(args.path_logs, args.path), index=False)
