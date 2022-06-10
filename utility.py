import pandas as pd
import unicodedata
import sqlite3
from numpy import int64

#全角文字にスペース付与
def add_space_if_fw(text):
    if unicodedata.east_asian_width(text) in 'FWA':
        return text + ' '
    else:
        return text

#マスターからDF作成
def master2df(file_name, widths, names, usecols, fn):
    with open(file_name, 'r', encoding='cp932') as f:
        content = f.read()

    result = ''

    for ch in content:
        result += add_space_if_fw(ch)

    file_name_changed = f'changed_{file_name}.csv'

    with open(file_name_changed, mode='w', encoding='UTF-8') as f:
        f.write(result)

    df = pd.read_fwf(file_name_changed, widths=widths, names=names, usecols=usecols, encoding='UTF-8', dtype = str).fillna(fn)

    if file_name == 'USROUT':
        df['sup_name'] = df['sup_name'].str.strip()
    elif file_name == 'KANOUT':
        df = df.astype({'num': int64, 'k_num': int64, 'y_num': int64, 'h_num': int64})
        df['seban'] = df['seban'].str.strip()
        df['hinban'] = df['hinban'].str.strip()
        df['store'] = df['store'].str.strip()
        df['box'] = df['box'].str.strip()
    
    return df

#RUIOUT用DF作成
def ruiout2df(d):
    file_name = 'RUIOUT'

    with open(file_name, 'r', encoding='cp932') as f:
        content = ''
        while True:
            line = f.readline()
            if line == '':
                break
            b_line = line[:5]
            st_line = d * 40 + 77 + 1
            a_line = line[-st_line:-78]
            content += b_line + a_line + '\n'

    file_name_changed = f'changed_{file_name}.csv'

    with open(file_name_changed, mode='w', encoding='UTF-8') as f:
        f.write(content)

    widths = [5]
    names = ['ad']
    meisai_width = [6, 2, 1, 6, 2, 4, 5, 3, 6, 5]
    usecols = [0]
    m_cols = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    astype = {}
    for i in range(d):
        widths += meisai_width
        m_name = [f'n_bi{i}', f'n_bin{i}', f'h_kubun{i}', f'h_bi{i}', f'h_bin{i}', f'h_jikan{i}', f'noban{i}', f'hako{i}', f'nonyu{i}', f'aki{i}']
        names += m_name
        usecols += [j + 10 * i for j in m_cols]
        astype[f'hako{i}'] = int64
        astype[f'nonyu{i}'] = int64

    df = pd.read_fwf(file_name_changed, widths=widths, names=names, usecols=usecols, encoding='UTF-8', dtype = str).fillna(0)
    df = df.astype(astype)
    return df

#DFからtable作成
def df2table(db, df, drop, create, table_name):

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(drop)
    cur.execute(create)
    df.to_sql(table_name, con, if_exists='append', index=False)
    cur.execute(
        f'SELECT * FROM {table_name} LIMIT 5'
    )
    tables = cur.fetchall()
    con.close()
    return tables