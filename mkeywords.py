import pandas as pd
import os
from datetime import datetime, date


def mkeywords(df):
    path = os.getcwd() + 'data/keywords.txt'
    print(path)
    dfc = df.copy()
    f = open(path, 'r')
    allKeywords = f.read().lower().split('\n')
    f.close()
    print(allKeywords)
    '''
    output_set = set()
    for var in df["More Info"]:
        if var == keywords:
            output_set.add(set)
    '''
    dfnew = df['More Info']
    return dfnew


if __name__ == '__main__':
    dt = datetime.now().date()
    fd = datetime.strptime(str(dt), "%Y-%m-%d").date()
    base_path = os.getcwd() + '/data/BSE_{}_{}'
    path_csv = base_path.format(fd, fd) + '.csv'
    print(path_csv)
    df = pd.read_csv(path_csv)
    dfnew = mkeywords(df)
    print(dfnew)
