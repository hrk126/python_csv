# coding: cp932
import streamlit as st
import datetime
import requests
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode

st.set_page_config(layout='wide')
# ------------------sidebar-----------------------------------------------
shuketubi = st.sidebar.date_input('日付を入力', value=datetime.date.today())
bin = st.sidebar.selectbox('便を入力', [1, 2, 3, 4])
selected_item = st.sidebar.radio('処理を選択', ['リスト登録', '品番検索'])
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
    df_items = pd.DataFrame(items)
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
      }, inplace=True
    )
    st.session_state.df = df_items

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
        update_mode=GridUpdateMode.SELECTION_CHANGED
    )

    if len(aggrid_data['selected_rows']) == 1:
      register_button = st.button('選択した品番を登録')

      if register_button:
        del st.session_state.df
        ad = aggrid_data['selected_rows'][0]['かんＳＥＬＦ']
        url = 'http://127.0.0.1:8000/create/'
        payload = {
          'ad': ad,
          'num': 0,
          'num_all': 0,
          'cust_name': '',
          'due_date': '',
          'tonyu': 0,
          'inventory': 0,
          'afure': 0,
          'shuketubi': shuketubi.isoformat(),
          'bin': bin,
          'comment': ''
        }
        res = requests.post(url, json.dumps(payload))
        if res.status_code == 200:
          st.success('登録しました')
        else:
          st.error(f'問題が発生しました(status code: {res.status_code})')

# ------------------list-------------------------------------------------
elif selected_item == 'リスト登録':

  q = f'?day={shuketubi.isoformat()}'
  url = f'http://127.0.0.1:8000/data/{q}'
  res = requests.get(url)
  data = res.json()
  df_data = pd.DataFrame(data)
  df_data.rename(
      columns= {
        'id': 'ID',
        's_num': '集欠数',
        'num_all': '集欠数(全体)',
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
        'seban': '背番号',
        'hinban': '品番',
        'm_num': '収容数',
        'store': 'ストアアドレス',
        'k_num': '回転枚数',
        'y_num': '読取枚数',
        'h_num': '発注枚数',
      }, inplace=True
    )
  st.session_state.list = df_data

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
        update_mode=GridUpdateMode.VALUE_CHANGED
    )

    change_button = st.button('修正内容を登録')
    if change_button:
      df = aggrid_data['data']
    for row in df.itertuples():
        del st.session_state.list
        ad = aggrid_data['selected_rows'][0]['かんＳＥＬＦ']
        url = 'http://127.0.0.1:8000/create/'
        payload = {
          'ad': ad,
          'num': 0,
          'num_all': 0,
          'cust_name': '',
          'due_date': '',
          'tonyu': 0,
          'inventory': 0,
          'afure': 0,
          'shuketubi': shuketubi.isoformat(),
          'bin': bin,
          'comment': ''
        }
        res = requests.post(url, json.dumps(payload))
        if res.status_code == 200:
          st.success('登録しました')
        else:
          st.error(f'問題が発生しました(status code: {res.status_code})')


