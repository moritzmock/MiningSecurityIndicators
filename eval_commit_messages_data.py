import pandas as pd
from utils import detect_SecI
from tqdm import tqdm


def eval_commit_messages_data(path):
    data = pd.read_csv(path)

    key = 'SecI'

    df = pd.DataFrame(columns=data.keys().tolist())

    pbar = tqdm(total=len(data[data.notna()]), desc='Changing shape of data...')

    for idx, row in data[data.notna()].iterrows():
        SSATD_array = row[key].split(', ')
        pbar_2 = tqdm(total=len(SSATD_array), desc='Adding SecI rows...', leave=False)
        for SSATD in SSATD_array:
            row[key] = SSATD
            df.loc[len(df)] = row
            pbar_2.update(1)

        pbar_2.close()
        pbar.update(1)

    pbar.close()

    df.to_csv(path.replace('.csv', '_single.csv'), index=False)

if __name__ == '__main__':

    eval_commit_messages_data('logs_traverse_commit_messages/<project>.csv')



