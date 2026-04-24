I am building a Python app that reads CSV files using pandas.
I want to clean the data, remove empty rows, and save a new file.

Example code:

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.dropna(inplace=True)
df.to_csv("cleaned.csv", index=False)
```

I also want a short explanation of what the code does.