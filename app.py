# coding: cp932
import streamlit as st
import datetime
import requests
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode

st.set_page_config(layout="wide")

# ------------------sidebar-----------------------------------------------
with st.sidebar.form(key='item'):
  hinban: str = st.text_input('品番')
  store: str = st.text_input('置場')
  submit_button = st.form_submit_button(label='送信')

selected_item = st.sidebar.radio('処理を選択', ['リスト登録', '品番検索'])

# ------------------header-------------------------------------------------
st.title(selected_item)
# ------------------search-------------------------------------------------

if selected_item == '品番検索':

  if submit_button:
    
    q = f'?hinban={hinban}&store={store}'
    url = f'http://127.0.0.1:8000/masters/{q}'
    res = requests.get(url)
    items = res.json()
    df_items = pd.DataFrame(items)
    df_items.rename(
      columns={
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
    gb.configure_default_column(editable=True)
    gb.configure_grid_options(enableRangeSelection=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    aggrid_data = AgGrid(
        st.session_state.df,
        gridOptions=gb.build(),
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED
    )

    if len(aggrid_data['selected_rows']) > 0:
      register_button = st.button('選択した品番を登録')

      if register_button:
        
        st.success('登録しました')


elif selected_item == 'リスト登録':
  st.write('list')
