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


if __name__ == "__main__":
    args = parser()

    idx = 0

    df = pd.DataFrame(columns=['path', 'comment', 'SecI', 'hash', 'date', 'tag'])

    regex_comment = get_comment_regex("php")

    path_tags = "{}/{}.csv".format("logs_extract_tags", args.path)
    df_tags = pd.read_csv(path_tags)

    pbar = tqdm(total=len(df_tags),
                desc="Traversing commits for the project {}... ".format(args.path))

    repo = Repo(args.path)

    for idx, row in df_tags.iterrows():
        commit_hash = row['hash']
        commit_date = row['date']
        commit_tag = row['tag']

        repo.git.checkout(commit_hash)

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
                            new_row = {'path': path, 'comment': comment, 'SecI': elem, 'hash': commit_hash,
                                       "date": commit_date, 'tag': commit_tag}
                            df.loc[len(df)] = new_row

            pbar2.update(1)

        pbar2.close()
        pbar.update(1)

    pbar.close()
    df.to_csv("{}/{}.csv".format(args.path_logs, args.path), index=False)
