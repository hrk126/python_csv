import streamlit as st
import datetime
import requests
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode

with st.form(key='item'):
  name: str = st.text_input('NAME', max_chars=3)
  code: int = st.number_input('CODE', step=1, min_value=1)
  submit_button = st.form_submit_button(label='SEND')

if submit_button:
  data = {
    'name': name,
    'code': code
  }
  url = 'http://127.0.0.1:8000/'
  res = requests.post(
    url,
    data = json.dumps(data)
  )


res = requests.get('http://127.0.0.1:8000/')
items = res.json()
df_items = pd.DataFrame(items)
# st.table(df_items)
# AgGrid(df_items)
gb = GridOptionsBuilder.from_dataframe(df_items)
gb.configure_default_column(editable=True)
gb.configure_grid_options(enableRangeSelection=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
aggrid_data = AgGrid(
    df_items,
    gridOptions=gb.build(),
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED
)
if len(aggrid_data['selected_rows']) != 0:
  st.write('selected')
  # for item in data['selected_rows']:
  #   st.write(item['name'])
  #   st.write(item['code'])
  #   st.write(item['id'])