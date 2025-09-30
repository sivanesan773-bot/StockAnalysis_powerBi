import pandas as pd
from pathlib import Path

rootPath = Path("CSV")
folder_path = Path("Visuvalization_excels")
wholedf = pd.DataFrame()
closeValue= []
volatileStock_List = []
cumulativereturns_list = []
ticker_List = []
# z = 0

def calcuclateVolatile(df) :

  ticker = df["Ticker"].to_list()
  df['Daily_Return'] = df['close'].pct_change()
  std_dev_daily_return = df['Daily_Return'].std()
  std_dev_percent = std_dev_daily_return * 100
  cumulative_return = (1 + df['Daily_Return'].fillna(0)).prod() - 1
  cumulative_return_percent = cumulative_return * 100
  return(std_dev_percent,cumulative_return_percent,ticker[0])

def volatileCheck() :
    for file in rootPath.iterdir():
        # print(f" {file.name}")
        df = pd.read_csv(f"CSV/{file.name}")
        volatileStock,cumulativereturns,ticker=calcuclateVolatile(df)
        volatileStock_List.append(volatileStock)
        cumulativereturns_list.append(cumulativereturns)
        ticker_List.append(ticker)

        
    wholedf['Ticker'] = ticker_List
    wholedf['Volatile value'] = volatileStock_List
    # print(wholedf)
    file_path = folder_path / "stock_Volatile_report.xlsx"
    wholedf.to_excel(file_path, index=False)
    wholedf['cumulative Returns'] = cumulativereturns_list
    file_path = folder_path / "cumulative_returns_report.xlsx"
    wholedf.to_excel(file_path, index=False)
    print(f"DataFrame saved to {file_path}")

volatileCheck()