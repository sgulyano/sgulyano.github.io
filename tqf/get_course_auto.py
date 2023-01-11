import os
import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

import argparse
parser = argparse.ArgumentParser(description='Scrap TQF 3 or 5 from reg.tu.ac.th')
parser.add_argument("tqf", help="TQF Type (either 3 or 5)", type=int)
parser.add_argument("o", help="Output CSV File", type=str)
args = parser.parse_args()

print('==================')
print(f'TQF: {args.tqf}')
print(f'Output file: {args.o}')
print('==================')

URL1 = 'https://web.reg.tu.ac.th/wwwtqf/coursespec.aspx'
MAX_ITER = 10000

s = requests.Session()
r = s.get(URL1)

data = {
    'pageNumber': 1,
    'itemPerPage': 0,
    'in_coursesemesterid': '',
    'in_classid': '',
    'in_tqftype': '0%d' % (args.tqf),
    'in_pagemode': 'P'
}
# print(data)


# resume from previous search, 
if args.tqf == 3:
    cid_file = 'tqf3_id.txt'
    cid = 168196
elif args.tqf == 5:
    cid_file = 'tqf5_id.txt'
    cid = 661456
else:
    raise Exception('Unknown TQF')


if os.path.exists(cid_file):
    with open(cid_file, 'r') as f:
        cid = int(f.readline())

# get previous result
prev_df = None
if os.path.exists(args.o):
    prev_df = pd.read_csv(args.o, encoding='utf-8')
    # cid = prev_df['classid'].max()
    # if len(prev_df) > 0:
    #     year = datetime.date.today().year-1+543
    #     cid = prev_df[prev_df['Year']>=year]['classid'].min()

# en_ind = cid + MAX_ITER

course_data = []

for cid in range(cid, cid + MAX_ITER):
    # retrieve data from reg
    if args.tqf == 3:
        data['in_coursesemesterid'] = str(cid)
    elif args.tqf == 5:
        data['in_classid'] = str(cid)
    else:
        raise Exception('Unknown TQF')

    URL2 = 'https://web.reg.tu.ac.th/wwwtqf/coursespec.aspx?__uikWsMth=AJAXWS_CourseSpecList'

    p = s.post(URL2, data=data)

    # couldn't find info, skip
    if p.status_code == 500:    
        s = requests.Session()
        r = s.get(URL1)
        print(cid, ' Status Code 500 ---> Skipped')
        # cid = cid + 1
        continue
    
    # extract info 
    div_text = json.loads(p.text)
    
    if div_text['body']:
        course_id_soup = BeautifulSoup(div_text['body'][1], 'html.parser')
        
        course_id = course_id_soup.findAll('tr')[-2:]
        th_name = course_id[0].text.strip()
        en_name = course_id[1].text.strip()
        
        semyear_soup = BeautifulSoup(div_text['body'][5], 'html.parser')
        semyear = semyear_soup.findAll('tr')[1].text.strip()
        
        year_regex = re.search('[0-9][0-9][0-9][0-9]', semyear)
        if year_regex:
            year = year_regex.group(0)
        else:
            year = ''
        
        if args.tqf == 5:
            sec_soup = BeautifulSoup(div_text['body'][4], 'html.parser')
            sec_regex = re.search('[0-9][0-9][0-9][0-9][0-9][0-9]', sec_soup.text)
            if sec_regex:
                sec = sec_regex.group(0)
            else:
                sec = ''
        
        print(f'[{cid}] {en_name}, Year: {year}')

        with open(cid_file, 'w') as f:
            f.write(str(cid))

        if args.tqf == 3:
            if en_name.strip().startswith('DSI'):
                course_data.append((cid, th_name, en_name, semyear, year))
        elif args.tqf == 5:
            if en_name.strip().startswith('DSI') or sec.strip().startswith('65050'):
                course_data.append((cid, th_name, en_name, semyear, sec, year))
        
        # en_ind = cid + MAX_ITER
    # cid = cid + 1

# save to csv
if args.tqf == 3:
    df = pd.DataFrame(course_data, columns=['classid', 'TH_name', 'EN_name', 'Semester', 'Year'])
elif args.tqf == 5:
    df = pd.DataFrame(course_data, columns=['classid', 'TH_name', 'EN_name', 'Semester', 'Section', 'Year'])

# merge previous record with the new one
if prev_df is not None:
    print(df)
    df = pd.concat([prev_df, df]).drop_duplicates(subset=['classid'], keep='last').sort_values(by=['classid'])

df.to_csv(args.o, index=None, encoding='utf-8')
print('Done')