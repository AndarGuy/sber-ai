import os

import pandas as pd

path = '/Users/mikhail/Desktop'

path_fin = '/Users/mikhail/Desktop/final.csv'

files = os.listdir(path)

final = pd.DataFrame()

for i in files:
    if i[-3:] == 'csv':
        print(i)
        try:
            final = pd.concat([pd.read_csv(path + '/' + i, encoding='utf_8'), final], axis=0, sort=True)
        except:
            try:
                final = pd.concat([pd.read_csv(path + '/' + i, encoding='cp1251'), final], axis=0, sort=True)
            except:
                pass

final.to_csv(path_fin, encoding='utf_8')
print(final)