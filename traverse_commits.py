from pydriller import Repository
from utils import detect_SecI, \
    parser
import pandas as pd
from tqdm import tqdm





if __name__ == '__main__':

    args = parser()

    idx = 0

    df = pd.DataFrame(columns=['date', 'message', 'SecI'])

    pbar = tqdm(desc="Traversing commits for the project {}... ".format(args.path))

    for commit in Repository(args.path).traverse_commits():
        pbar.update(1)
        idx = idx + 1
        commit_message = commit.msg

        vector = detect_SecI(commit_message)

        if len(vector) > 0:
            new_row = {'date': commit.committer_date, 'message': commit_message, 'SecI': ", ".join(vector)}
            df.loc[len(df)] = new_row

    df.to_csv("{}/{}.csv".format(args.path_logs, args.path), index=False)
