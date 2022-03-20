import streamlit as st
import datetime
import requests
import json
import pandas as pd

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
st.table(df_items)