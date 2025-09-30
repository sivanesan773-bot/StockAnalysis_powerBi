# Stock Analysi Report
As an in put one year(Nov'23 - Nov'24) NIFTY - 50 details is given as Yaml file

# step 1 => converted all Yaml file and grouped Company wise and converted to CSV file [convertYamlToCsv.py]
csv stored in Company_csv folder

# step 2 => Cumulative & volatile
The cumulative & volatile value for all 50 Company is calculated aand stored as separate excel under Visuvalization_excel folder [volatility_cumulative_Check.py]

# step 3 = > sectorwise performance & MOst correlated task
we have a separate excel for ticker sector mapping, 
Have combined all 50 csv into single dataframe and added sector value based on ticker value then we calculated the returns based on sector and most correlated company and its value [sectorwisePerformance_correlation.py]

# step 4 => Top 5 gain & loss

By using the wholeDF calculated top 5 gainer and looser month wise and stored in separate excel [gainedLooser.py]

# Result Excel :
All the result for above script is stored in folder => Visuvalization_excel

# PowerBI visuvalization is designed and stored in folder => power_BI_Visuvalization

# The result of above script is stored in MySQL db under schema : stock as 6 different table

# By using the MySql DB Have created dashbord covering below metrics using STREAMLIT framework under python
     => Most volatile Stock
     => Top 10 cumulative returs and stock
     => Sector wise representation and returns
     => Most correlated Stocks and its value
     => Top 5 gainer & Looser month wise splitup (Total 24 Visuvalization)
