from pydriller import Repository
from utils import parser, \
    read_file, \
    get_comment_regex, \
    detect_SecI, \
    find_files, \
    has_task_words_values, \
    get_mat
import pandas as pd
from tqdm import tqdm
from git import Repo


def get_number_of_commits(path):
    count = 0
    for _ in Repository(path).traverse_commits():
        count += 1

    return count


if __name__ == "__main__":
    args = parser()

    idx = 0

    df = pd.DataFrame(columns=['path', 'comment', 'SecI', 'hash', 'date'])

    regex_comment = get_comment_regex("php")

    repo = Repo(path=args.path)

    pbar = tqdm(total=get_number_of_commits(args.path),
                desc="Traversing commits for the project {}... ".format(args.path))

    for commit in Repository(args.path, order='date-order').traverse_commits():
        repo.git.checkout(commit.hash)

        file_extensions = ['.php']  # Maybe consider also other extensions
        paths = find_files(args.path, file_extensions[0], leave=False)

        pbar2 = tqdm(total=len(paths), leave=False, desc="Traversing files of the project {}...".format(args.path))

        for path in paths:
            # only considers files with the extension .php
            file_content = read_file(path)

            if file_content is None:
                print("SKIPPING {}".format(path))
            else:
                comments = [comment[0] for comment in regex_comment.findall(file_content)]

                for comment in comments:
                    vector = detect_SecI(comment) if args.MAT == False else has_task_words_values(comment,
                                                                                                  patterns=get_mat())

                    if len(vector) > 0:
                        for elem in vector:
                            new_row = {'path': path, 'comment': comment, 'SecI': elem, 'hash': commit.hash,
                                       "date": commit.committer_date}
                            df.loc[len(df)] = new_row

            pbar2.update(1)

        pbar2.close()
        pbar.update(1)

    pbar.close()
    df.to_csv("{}/{}.csv".format(args.path_logs, args.path), index=False)
