from utils import parser
from pydriller import Git
import pandas as pd
from subprocess import PIPE
import subprocess
from tqdm import tqdm

if __name__ == "__main__":

    args = parser()

    repo = Git(args.path)

    tagged_commits = repo.get_tagged_commits()

    tags = subprocess.check_output(["git", "tag"], cwd=args.path)

    tags = tags.decode('latin1')

    tags = tags.split('\n')

    df = pd.DataFrame(columns=["tag", "hash", "date"])

    pbar = tqdm(total=len(tags), desc='Extracting tags...')

    for tag in tags:
        if tag != '':
            commit = repo.get_commit_from_tag(tag)

            new_row = {'tag': tag, 'hash': commit.hash, 'date': commit.committer_date}
            df.loc[len(df)] = new_row

        pbar.update(1)

    pbar.close()

    df.to_csv('{}/{}.csv'.format(args.path_logs, args.path), index=False)


