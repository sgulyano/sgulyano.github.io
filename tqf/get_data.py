import re
import os
import json
import datetime
import pandas as pd

import argparse
parser = argparse.ArgumentParser(description='Merge course lists from TQF3 and TQF5 for displaying on website.')
parser.add_argument("tqf3", help="TQF 3 course list file", type=str)
parser.add_argument("tqf5", help="TQF 5 course list file", type=str)
parser.add_argument("o", help="Output folder", type=str)
args = parser.parse_args()

print('==================')
print(f'TQF3: {args.tqf3}')
print(f'TQF5: {args.tqf5}')
print(f'Output folder: {args.o}')
print('==================')

tqf3 = pd.read_csv(args.tqf3, encoding='utf-8')
tqf5 = pd.read_csv(args.tqf5, encoding='utf-8')

# check only the 5 previous academic year
year = datetime.date.today().year-4+543
month = datetime.date.today().month
if month <= 9:
    year = year-1
tqf3 = tqf3[tqf3['Year']>=year]
tqf5 = tqf5[tqf5['Year']>=year]


def get_sem(s):
    res = re.findall('ภาคการศึกษาที่\s*(\d)', s)
    if res:
        return res[0]
    return ''

# tqf3['TH_name'] = tqf3['TH_name'].apply(lambda x: x.strip())
tqf3_clean = pd.concat([tqf3['classid'], 
                        tqf3['TH_name'].str.split("\n", n = 1, expand = True),
                        tqf3['EN_name'].str.split("\n", n = 1, expand = True),
                        tqf3['Semester'].apply(get_sem),
                        tqf3['Year']], axis=1)


tqf3_clean.columns = ['ID', 'TH_code', 'TH_name', 'EN_code', 'EN_name', 'Sem', 'Year']
tqf3_clean['EN_code'] = tqf3_clean['EN_code'].str.strip()
tqf3_clean['TH_code'] = tqf3_clean['TH_code'].str.strip()


tqf5_clean = pd.concat([tqf5['classid'], 
                        tqf5['TH_name'].str.split("\n", n = 1, expand = True),
                        tqf5['EN_name'].str.split("\n", n = 1, expand = True),
                        tqf5['Section'],
                        tqf5['Semester'].apply(get_sem),
                        tqf5['Year']], axis=1)
tqf5_clean.columns = ['ID', 'TH_code', 'TH_name', 'EN_code', 'EN_name', 'Section', 'Sem', 'Year']
tqf5_clean['EN_code'] = tqf5_clean['EN_code'].str.strip()
tqf5_clean['TH_code'] = tqf5_clean['TH_code'].str.strip()

# print(tqf3_clean)
# df = pd.concat([tqf3_clean, tqf5_clean], axis=0)
# df = pd.concat([tqf5_clean, tqf3_clean[~tqf3_clean['EN_code'].isin(tqf5_clean['EN_code'])]], axis=0)

for y in sorted(pd.concat([tqf3['Year'], tqf5['Year']]).unique()):
    # df_cur = df[df['Year'] == y]
    tqf3_cur = tqf3_clean[tqf3_clean['Year'] == y]
    tqf5_cur = tqf5_clean[tqf5_clean['Year'] == y]
    df = pd.concat([tqf5_cur, tqf3_cur[~tqf3_cur['EN_code'].isin(tqf5_cur['EN_code'])]], axis=0)

    # df = pd.concat([tqf5_clean, tqf3_clean[~tqf3_clean['EN_code'].isin(tqf5_clean['EN_code'])]], axis=0)
    
    
    # fp = '%d.json' % (y)
    # if os.path.exists(fp):
    #     # combine with previous file
    #     with open(fp, 'r') as f:
    #         prev_data = json.load(f)
    #     df_prev = pd.DataFrame(prev_data)
        
    #     df_new = pd.concat([df_prev, df_cur[~df_cur['ID'].isin(df_prev['ID'])]], axis=0)
    #     df_new = df_new.sort_values(['EN_code', 'Section', 'ID'])

    # else:
    #     df_new = df_cur.sort_values(['EN_code', 'Section', 'ID'])
    
    df_new = df.sort_values(['Sem', 'EN_code', 'Section', 'ID'])

    # print(y, df_new)

    with open(os.path.join(args.o, '%d.json' % (y)), 'w', encoding='utf-8') as f:
        f.write(df_new.to_json(orient="records"))
    print(os.path.abspath(os.path.join(args.o, '%d.json' % (y))), 'Done')