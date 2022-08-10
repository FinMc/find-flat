import pandas as pd
import_csv = pd.read_csv("public/save.csv")
for l, v in import_csv.iterrows():
    print(v.values.tolist()[1:])
    break