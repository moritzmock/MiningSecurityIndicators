import pandas as pd
from tqdm import tqdm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import parser
from pydriller import Repository

def find_first_commit_after(data, date):
    date_objects = [datetime.strptime(timestamp[:-6], '%Y-%m-%d %H:%M:%S').replace(tzinfo=None) for timestamp in data["date"].tolist()]
    # Filter timestamps that are larger than the specific date
    larger_timestamps = [timestamp for timestamp in date_objects if timestamp > date]
    # Find the smallest timestamp among the larger ones
    return min(larger_timestamps) if larger_timestamps else None


if __name__ == '__main__':

    args = parser()

    data = pd.read_csv("{}/{}.csv".format(args.path_logs, args.path))

    df = pd.DataFrame(columns=['path', 'comment', 'SecI', 'months', 'resolved', 'created', 'removed'])

    df_hashes = pd.read_csv("{}/{}.csv".format("logs_extract_tags", args.path))

    unique_data = data[['path', 'comment', 'SecI']].drop_duplicates()
    unique_data = data.iloc[unique_data.index.tolist()]

    pbar = tqdm(total=len(unique_data), desc="Evaluating...")

    for row in unique_data.itertuples():
        path = row.path
        comment = row.comment
        SecI = row.SecI
        date = row.date
        interim_df = data[(data["path"] == path) &
                          (data["comment"] == comment) &
                          (data["SecI"] == SecI)]

        if len(interim_df) > 1:
            all_dates = interim_df["date"].tolist()
            date_objects = [datetime.strptime(timestamp[:-6], '%Y-%m-%d %H:%M:%S') for timestamp in all_dates]
            largest_timestamp = max(date_objects)
            smallest_timestamp = min(date_objects)
            next = find_first_commit_after(df_hashes, largest_timestamp)
            difference_in_months = 0
            resolved = False
            if next is not None:
                difference_in_years = next.year - smallest_timestamp.year
                difference_in_months = difference_in_years * 12 + (next.month - smallest_timestamp.month)

                resolved = True
            else:
                difference_in_years = datetime.today().year - smallest_timestamp.year
                difference_in_months = difference_in_years * 12 + (datetime.today().month - smallest_timestamp.month)

            new_row = {'path': path, 'comment': comment, 'SecI': SecI, 'months': difference_in_months, 'resolved': resolved,
                       'created': smallest_timestamp,
                       'removed': datetime.strptime(next.strftime('%Y-%m-%d %H:%M:%S') if next is not None else
                                                    datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')}
            df.loc[len(df)] = new_row

        pbar.update(1)


    pbar.close()

    df.to_csv("{}/{}_eval.csv".format(args.path_logs, args.path), index=False)
