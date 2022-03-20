import pandas as pd
import unicodedata

def add_space_if_fw(text):
  if unicodedata.east_asian_width(text) in 'FWA':
    return text + ' '
  else:
    return text


file_name = 'test.csv'

with open(file_name, 'r', encoding='UTF-8') as f:
  content = f.read()

result = ''

for ch in content:
  result += add_space_if_fw(ch)

with open(file_name, mode="w", encoding="UTF-8") as f:
    f.write(result)

colspecs = [2,2,2]
col_name = ['id1', 'id2', 'id3']
df = pd.read_fwf(file_name, colspecs=colspecs, names=col_name, encoding='UTF-8')

print(df)


