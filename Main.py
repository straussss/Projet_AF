import pandas as pd
df = pd.read_csv("Data/data.csv", index_col='Unnamed: 0')
df = df.rename(columns={"Close":"BTC"})
print(df)