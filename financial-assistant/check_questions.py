import pandas as pd

# 读取附件4
df = pd.read_excel('附件4.xlsx')
print(f'问题数量: {len(df)}')
print('列名:', df.columns.tolist())
print('\n所有问题:')
for idx, row in df.iterrows():
    qid = str(row.get('问题编号', f'B{idx+1:03d}')).strip()
    question = str(row.get('问题', row.iloc[0])).strip()
    print(f'{qid}: {question}')
