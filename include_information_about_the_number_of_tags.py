import pandas as pd
from utils import parser
from tqdm import tqdm

def get_index(data, value):
    row = data[data["date"] == value]
    if len(row) == 0:
        return -1
    if len(row) == 1:
        return row.index[0]

    print("ERROR: more than one tag was found!")
    quit()

if __name__ == "__main__":
    args = parser()

    data_tags = pd.read_csv("./logs_extract_tags/{}.csv".format(args.path))
    data_tags = data_tags.sort_values(by="date", ascending=False)
    data_tags = data_tags.reset_index(drop=True)
    data_tags['date'] = data_tags['date'].apply(lambda x:x[:-6])


    data = pd.read_csv("./{}/{}_eval.csv".format(args.path_logs, args.path))
    data['age'] = -1

    pbar = tqdm(total=len(data), desc="Evaluating tags for the number of tags they stayed....")

    for idx, row in data.iterrows():
        created = row['created']
        removed = row['removed']
        index_created = get_index(data_tags, created)
        index_removed = get_index(data_tags, removed)
        age = index_created-index_removed
        data.loc[idx, 'age'] = age
        pbar.update(1)

    pbar.close()

    data.to_csv("./{}/{}_eval_new.csv".format(args.path_logs, args.path))
