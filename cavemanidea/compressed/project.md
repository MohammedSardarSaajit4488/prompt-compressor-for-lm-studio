i build app python. read csv. clean rows empty. save new file.

code:
import pandas as pd
df = pd.read_csv("data.csv")
df.dropna(inplace=True)
df.to_csv("cleaned.csv", index=False)