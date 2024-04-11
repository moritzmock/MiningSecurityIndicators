import os
from tqdm import tqdm
from utils import parser, \
    read_file, \
    get_comment_regex, \
    detect_SecI, \
    find_files
import pandas as pd

if __name__ == "__main__":

    args = parser()

    file_extensions = ['.php']  # Maybe consider also other extensions

    paths = find_files(args.path, file_extensions[0])

    regex_comment = get_comment_regex("php")

    df = pd.DataFrame(columns=['path', 'comment', 'SecI'])

    pbar = tqdm(total=len(paths), desc="Scanning files...")

    for path in paths:
        pbar.update(1)
        file_content = read_file(path)
        if file_content is None:
            print("SKIPPING {}".format(path))
        else:
            comments = [comment[0] for comment in regex_comment.findall(file_content)]
            for comment in comments:
                vector = detect_SecI(comment)

                if len(vector) > 0:
                    for element in vector:
                        new_row = {'path': path, 'comment': comment, 'SecI': element}
                        df.loc[len(df)] = new_row

    pbar.close()

    df.to_csv("{}/{}.csv".format(args.path_logs, args.path), index=False)