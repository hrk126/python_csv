import pandas as pd
import unicodedata

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
        df = df.astype({'num': int, 'k_num': int, 'y_num': int, 'h_num': int})
        df['seban'] = df['seban'].str.strip()
        df['hinban'] = df['hinban'].str.strip()
        df['store'] = df['store'].str.strip()
        df['box'] = df['box'].str.strip()
    
    return df