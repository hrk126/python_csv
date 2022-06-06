# coding: cp932
from re import U
import streamlit as st
import datetime
import requests
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
import base64
import sqlite3
import utility as utl

st.set_page_config(layout='wide')

# ------------------sidebar-----------------------------------------------
shuketubi = st.sidebar.date_input('日付を入力', value=datetime.date.today())
bin = st.sidebar.selectbox('便を入力', [1, 2, 3, 4])
selected_item = st.sidebar.radio('処理を選択', ['リスト登録', '品番検索', 'マスタ更新'])

# ------------------header-------------------------------------------------
st.title(selected_item)

# ------------------search-------------------------------------------------
if selected_item == '品番検索':

  with st.sidebar.form(key='item'):
    hinban: str = st.text_input('品番')
    store: str = st.text_input('置場')
    submit_button = st.form_submit_button(label='送信')

  if submit_button:
    
    q = f'?hinban={hinban}&store={store}'
    url = f'http://127.0.0.1:8000/masters/{q}'
    res = requests.get(url)
    items = res.json()
    if len(items) != 0: 
      df_items = pd.DataFrame(items)
      df_items = df_items.reindex(columns=[
        'id', 'ad', 'sup_code', 'sup_name', 'hinban', 'seban', 'store', 'num', 'box', 'k_num', 'y_num', 'h_num'
      ])
      df_items.rename(
        columns= {
          'ad': 'かんＳＥＬＦ',
          'sup_code': '仕入先',
          'seban': '背番号',
          'hinban': '品番',
          'num': '収容数',
          'store': 'ストアアドレス',
          'k_num': '回転枚数',
          'y_num': '読取枚数',
          'h_num': '発注枚数',
          'box': '箱種',
          'sup_name':'仕入先名'
        }, inplace=True
      )
      st.session_state.df = df_items
    else:
      if 'df' in st.session_state:
        del st.session_state.df
      st.write('見つかりませんでした')

  if 'df' in st.session_state: 

    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    # gb.configure_default_column(editable=True)
    gb.configure_grid_options(enableRangeSelection=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    aggrid_data = AgGrid(
        st.session_state.df,
        gridOptions=gb.build(),
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED
    )

    if len(aggrid_data['selected_rows']) == 1:

      st.write('追加情報を入力')
      num: int = st.text_input('集欠数', value=0)
      num_all: int = st.text_input('集欠数_全体', value=0)
      cust_name: str = st.text_input('得意先名', value='')
      due_date: datetime.date = st.date_input('期日', value=datetime.date.today())
      tonyu: int = st.text_input('投入数', value=0)
      inventory: int = st.text_input('在庫数', value=0)
      afure: int = st.text_input('あふれ数', value=0)
      comment: str = st.text_input('コメント', value='')

      register_button = st.button('選択した品番を登録')

      if register_button:
        del st.session_state.df
        ad = aggrid_data['selected_rows'][0]['かんＳＥＬＦ']
        url = 'http://127.0.0.1:8000/create/'
        payload = {
          'ad': ad,
          'num': num,
          'num_all': num_all,
          'cust_name': cust_name,
          'due_date': due_date.isoformat(),
          'tonyu': tonyu,
          'inventory': inventory,
          'afure': afure,
          'shuketubi': shuketubi.isoformat(),
          'bin': bin,
          'comment': comment
        }
        res = requests.post(url, json.dumps(payload))
        if res.status_code == 200:
          st.success('登録しました')
        else:
          st.error(f'問題が発生しました(status code: {res.status_code})')

# ------------------list---------------------------------------------------
elif selected_item == 'リスト登録':

  q = f'?day={shuketubi.isoformat()}'
  url = f'http://127.0.0.1:8000/data/{q}'
  res = requests.get(url)
  data = res.json()
  if len(data) != 0:
    df_data = pd.DataFrame(data)
    df_data.rename(
        columns= {
          'id': 'ID',
          's_num': '集欠数',
          'num_all': '集欠数_全体',
          'cust_name': '得意先名',
          'due_date': '期日',
          'tonyu': '投入数',
          'inventory': '在庫数',
          'afure': 'あふれ数',
          'shuketubi': '集欠日',
          'bin': '集欠便',
          'comment': 'コメント',
          'ad': 'かんＳＥＬＦ',
          'sup_code': '仕入先',
          'sup_name': '仕入先名',
          'seban': '背番号',
          'hinban': '品番',
          'm_num': '収容数',
          'store': 'ストアアドレス',
          'k_num': '回転枚数',
          'y_num': '読取枚数',
          'h_num': '発注枚数',
          'box': '箱種'
        }, inplace=True
      )
    st.session_state.list = df_data
  else:
    if 'list' in st.session_state:
      del st.session_state.list
    st.write('対象のリストはありません')

  if 'list' in st.session_state: 

    gb = GridOptionsBuilder.from_dataframe(st.session_state.list)
    gb.configure_default_column(editable=True)
    gb.configure_grid_options(enableRangeSelection=True)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True)
    aggrid_data = AgGrid(
        st.session_state.list,
        gridOptions=gb.build(),
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED
    )
    # 修正ボタン
    change_button = st.button('修正内容を登録')
    if change_button:
      df = aggrid_data['data']
      del st.session_state.list
      url = 'http://127.0.0.1:8000/data/update/'
      payload = []
      for id, ad, shuketubi, bin, num, num_all, cust_name, due_date, tonyu, inventory, afure, comment in \
      zip(df['ID'],
          df['かんＳＥＬＦ'],
          df['集欠日'],
          df['集欠便'],
          df['集欠数'],
          df['集欠数_全体'],
          df['得意先名'],
          df['期日'],
          df['投入数'],
          df['在庫数'],
          df['あふれ数'],
          df['コメント']):
          buf = {
            'id': id,
            'ad': ad,
            'shuketubi': shuketubi,
            'bin': bin,
            'num': num,
            'num_all': num_all,
            'cust_name': cust_name,
            'due_date': due_date,
            'tonyu': tonyu,
            'inventory': inventory,
            'afure': afure,
            'comment': comment
          }
          payload.append(buf)
      res = requests.post(url, json.dumps(payload))
      if res.status_code == 200 and res.json()['message'] == 'update success':
        st.success('登録しました')
      else:
        st.error(f'問題が発生しました(status code: {res.status_code})')

    # 削除ボタン
    delete_button = st.button('選択を削除')
    if delete_button:
      if len(aggrid_data['selected_rows']) > 0:
        del st.session_state.list
        url = 'http://127.0.0.1:8000/data/delete/'
        payload = []
        for row in aggrid_data['selected_rows']:
          payload.append(row['ID'])
        res = requests.post(url, json.dumps(payload))
        if res.status_code == 200 and res.json()['message'] == 'delete success':
          st.success('削除しました')
        else:
          st.error(f'問題が発生しました(status code: {res.status_code})')

    # CSVダウンロード
    csv = aggrid_data['data'].to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    d = datetime.date.today().isoformat()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="shuketu_list{d}.csv">CSVファイルのダウンロード</a>'
    st.markdown(href, unsafe_allow_html=True)

# ------------------master-------------------------------------------------
elif selected_item == 'マスタ更新':

  db = 'test.db'

  #マスタ
  st.markdown('### ● マスタアップロード(KANOUT)')
  file = st.file_uploader('マスタをアップロードしてください.')
  if file:
    if file.name == 'KANOUT':
      file_name = file.name
      widths = [1, 5, 1, 1, 5, 2, 4, 14, 5, 8, 5, 1, 10, 4, 5, 2, 1, 3, 6, 2, 4, 8, 5, 6, 4, 8, 4, 3, 4, 4, 8, 4, 4, 4, 5, 5, 5, 5, 5, 5, 8, 1, 1, 2, 1, 8, 10, 8, 12, 1, 3, 1, 9]
      names = ['aki', 'ad', 'kaitei', 'cp', 'sup_code', 'ukeire', 'seban', 'hinban', 'num', 'store', 'sikyu', 's_kubun', 'line_add', 'aki2', 'shuyoseki', 'tanto', 'iro', 'pocket', 'cycle', 'aki3', 'setteimai', 'setteiryo', 'mai_bin', 'ryo_bin', 'zen_mai', 'zen_ryo', 'k_num', 'y_num', 's_num', 'h_num', 'sohat', 'kinko', 'hakko', 'hakkosumi', 'b_add', 'a_add', 'gai_1', 'gai_2', 'gai_3', 'siharai', 'kigo', 'b_kubun', 'u_kubun', 'mark', 'mark_col', 'box', 'kose', 's_okiba', 'comment', 'sys_kubun', 'shukkaba', 'n_kubun', 'aki4']
      usecols= [1, 4, 6, 7, 8, 9, 26, 27, 29, 45]
      fn = {
        'num': 0,
        'k_num': 0,
        'y_num': 0,
        'h_num': 0,
        'ad': '',
        'sup_code': '',
        'seban': '',
        'hinban': '',
        'store': '',
        'box': ''
      }
      with open(file.name, 'wb') as f:
          f.write(file.read())
      df = utl.master2df(file_name, widths, names, usecols, fn)
      drop = 'DROP TABLE IF EXISTS master'
      create = '''
                CREATE TABLE master (
                  id INTEGER PRIMARY KEY, 
                  ad TEXT, 
                  sup_code TEXT, 
                  seban TEXT, 
                  hinban TEXT, 
                  num INTEGER, 
                  store TEXT, 
                  k_num INTEGER, 
                  y_num INTEGER, 
                  h_num INTEGER,
                  box TEXT
                )
               '''
      table_name = 'master'
      tables = utl.df2table(db, df, drop, create, table_name)
      st.table(tables)

  #仕入先マスタ
  st.markdown('### ● 仕入先アップロード(USROUT)')
  file = st.file_uploader('仕入先をアップロードしてください.')
  if file:
    if file.name == 'USROUT':
      file_name = file.name
      widths = [6, 5, 20]
      names = ['ad', 'sup_code', 'sup_name']
      usecols= [1, 2]
      fn = 0
      with open(file.name, 'wb') as f:
          f.write(file.read())
      df = utl.master2df(file_name, widths, names, usecols, fn)
      drop = 'DROP TABLE IF EXISTS sup'
      create = '''
                CREATE TABLE sup (
                  id INTEGER PRIMARY KEY, 
                  sup_code TEXT,
                  sup_name TEXT
                )
               '''
      table_name = 'sup'
      tables = utl.df2table(db, df, drop, create, table_name)
      st.table(tables)

  #累積マスタ
  st.markdown('### ● 発注累積アップロード(RUIOUT)')
  file = st.file_uploader('発注累積をアップロードしてください.')
  if file:
    if file.name == 'RUIOUT':
      d = 3
      with open(file.name, 'wb') as f:
          f.write(file.read())
      df = utl.ruiout2df(d)
      drop = 'DROP TABLE IF EXISTS rui'
      s = ''
      for i in range(d):
          s += f'''
              n_bi{i} TEXT,
              n_bin{i} TEXT,
              h_kubun{i} TEXT,
              h_bi{i} TEXT,
              h_bin{i} TEXT,
              h_jikan{i} TEXT,
              noban{i} TEXT,
              hako{i} INTEGER,
              nonyu{i} INTEGER,'''
      s = s[:-1]
      create = f'''
          CREATE TABLE rui (
              id INTEGER PRIMARY KEY, 
              ad TEXT,{s}
          )
          '''
      table_name = 'rui'
      tables = utl.df2table(db, df, drop, create, table_name)
      st.table(tables)
