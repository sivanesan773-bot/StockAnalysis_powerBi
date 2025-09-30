from pathlib import Path
import pandas as pd
import yaml
import re
wholedf = pd.DataFrame()
sectorData = pd.DataFrame()
rootFolder = Path("data")
sectorDict = {}

sectorData= pd.read_csv('Sector_data - Sheet1.csv')

sector = sectorData["sector"].to_list()
symbol = sectorData["Symbol"].to_list()

for x,y in zip(symbol,sector) :
    x = x[x.index(":")+2:]
    sectorDict[x] = y

print(sectorDict)



for folder in rootFolder.iterdir():
    if folder.is_dir():   # check if it's a folder
        # print(f" Folder: {folder}")
        # you can also iterate inside each folder:
        for file in folder.iterdir():
            # print(f"    {file.name}")
            with open (file,"r") as yafile :
                yaml_data = yaml.safe_load(yafile)
            df = pd.DataFrame(yaml_data)
            wholedf = pd.concat([wholedf,df], ignore_index=True)
            print("dataframe added successfully")

for ticker, group in wholedf.groupby("Ticker"):
    filename = f"{ticker}.csv"
    group["sector"] = group["Ticker"].map(sectorDict)
    # print(group)
    group.to_csv(filename, index=False)   # index=False avoids writing row numbers
    print(f"✅ Saved {filename}")


print (wholedf)