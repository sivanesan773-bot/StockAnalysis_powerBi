import pandas as pd
from pathlib import Path
import yaml
import re

rootPath = Path("CSV")
folder_path = Path("Visuvalization_excels")
wholedf = pd.DataFrame()
rootFolder = Path("data")

for folder in rootFolder.iterdir():
    if folder.is_dir():    # check if it's a folder
        # print(f" Folder: {folder}")
        # you can also iterate inside each folder:
        for file in folder.iterdir():
            # print(f"    {file.name}")
            with open (file,"r") as yafile :
                yaml_data = yaml.safe_load(yafile)
            df = pd.DataFrame(yaml_data)
            wholedf = pd.concat([wholedf,df], ignore_index=True)
            print("dataframe added successfully")
# print(wholedf) # Commented out print
df = wholedf
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.sort_values(['Ticker', 'date']).dropna(subset=['date']).reset_index(drop=True)

monthly_prices = df.groupby('Ticker').resample('M', on='date')['close'].last().reset_index()
monthly_prices['Monthly_Return'] = monthly_prices.groupby('Ticker')['close'].pct_change()
returns_table = monthly_prices.pivot(index='date', columns='Ticker', values='Monthly_Return')
returns_table.index = returns_table.index.to_period('M').astype(str)
monthly_returns_pct = (returns_table * 100).round(2)
returns_series = monthly_returns_pct.stack().reset_index()
returns_series.columns = ['Month', 'Ticker', 'Return_PCT']
returns_series = returns_series.dropna(subset=['Return_PCT'])

#  below line only for gainer
# top_5_monthly = returns_series.groupby('Month').apply(lambda x: x.nlargest(5, 'Return_PCT')).reset_index(drop=True)

# , below line only for Looser
top_5_monthly = returns_series.groupby('Month').apply(lambda x: x.nsmallest(5, 'Return_PCT')).reset_index(drop=True)

#  below line only for gainer
# top_5_monthly = top_5_monthly.sort_values(by=['Month', 'Return_PCT'], ascending=[True, False]).reset_index(drop=True)


print(top_5_monthly)

file_path = folder_path / "looserTop5.xlsx"
top_5_monthly.to_excel(file_path, index=False)
print(f"DataFrame saved to {file_path}")