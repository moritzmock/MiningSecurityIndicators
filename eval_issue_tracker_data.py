import pandas as pd
from utils import detect_SecI
from tqdm import tqdm

def is_not_nan_float(value):
    if type(value) is not float:
        return True

    return False
def eval_issue_tracker_data(path, issue_tracker):
    data = pd.read_csv(path)

    key = None

    if issue_tracker == 'jira':
        key = 'description'
    elif issue_tracker == 'github':
        key = 'issue_desc'
    else:
        return None
    if 'SecI' not in data.keys():
        data['SecI'] = ''

        pbar = tqdm(total=len(data), desc='Evaluating issues...')

        for idx, row in data.iterrows():
            desc = row[key]
            if is_not_nan_float(desc):
                vector = detect_SecI(desc)
                data.loc[idx, 'SecI'] = '$'.join(vector)

            pbar.update(1)

        pbar.close()

        data.to_csv(path, index=False)

    df = pd.DataFrame(columns=data.keys().tolist())

    pbar = tqdm(total=len(data[data.notna()]), desc='Changing shape of data...')

    for idx, row in data[data.notna()].iterrows():
        if is_not_nan_float(row['SecI']):
            SecI_array = row['SecI'].split('$')
            pbar_2 = tqdm(total=len(SecI_array), desc='Adding SecI rows...', leave=False)
            for SecI in SecI_array:
                row['SecI'] = SecI
                df.loc[len(df)] = row
                pbar_2.update(1)

            pbar_2.close()
        pbar.update(1)

    pbar.close()

    df.to_csv(path.replace('.csv', '_single.csv'), index=False)
    print(len(df))


if __name__ == '__main__':

    eval_issue_tracker_data('logs_traverse_issue_tracker/glpi_github.csv', 'github')
    eval_issue_tracker_data('logs_traverse_issue_tracker/icingaweb2_github.csv', 'github')
    eval_issue_tracker_data('logs_traverse_issue_tracker/icingaweb2-module-pdfexport_github.csv', 'github')
    eval_issue_tracker_data('logs_traverse_issue_tracker/global_product_jira.csv', 'jira')
    eval_issue_tracker_data('logs_traverse_issue_tracker/icingaweb2-module-slm_jira.csv', 'jira')



