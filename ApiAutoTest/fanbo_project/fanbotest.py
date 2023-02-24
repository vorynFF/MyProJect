import pandas as pd


file_name = "android_af_cnt.csv"
df = pd.read_csv(file_name, encoding='utf-8', header=0, skipinitialspace=True)
print(df)

d2 = df.groupby(["mobile_marketing_name"])[["cnt"]].sum()

print(d2)

d2.reset_index().to_csv("taxout4.csv", index=False)