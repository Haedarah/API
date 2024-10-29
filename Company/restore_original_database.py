import pandas as pd

df = pd.read_excel('database/restore.xlsx',dtype=str) #read the original excel sheet
df.to_excel('database/users-points.xlsx', index=False) #save it as the original excel sheet

print("Done!")