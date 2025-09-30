import streamlit as st
import mysql.connector as mc
from datetime import date
import re
import cred
import pandas as pd
import json
import plotly.express as px

mydb = mc.connect(host=cred.sqlHost,user=cred.sqlUser,password=cred.sqlPword,database=cred.sqlDatabase)

mycursor = mydb.cursor()

def looser ():
    mycursor.execute(cred.looserTop5)
    dates = []
    company = []
    value = []
    for x in mycursor :
        dates.append(x[0])
        company.append(x[1])
        value.append(x[2])
    df  = pd.DataFrame({'dates':dates,'company':company,'value':value})
    return df

def gainer ():
    mycursor.execute(cred.gainerTop5)
    dates = []
    company = []
    value = []
    for x in mycursor :
        dates.append(x[0])
        company.append(x[1])
        value.append(x[2])
    df  = pd.DataFrame({'dates':dates,'company':company,'value':value})
    return df
def correlation ():
    company = []
    correlation_value = []
    mycursor.execute(cred.correlation_query)
    for x in mycursor :
        company.append(x[0]+" & "+x[1])
        correlation_value.append(x[2])
    df  = pd.DataFrame({'company':company,'correlation_value':correlation_value})
    return df

def sector():
    sector = []
    sector_value = []
    mycursor.execute(cred.sector_query)
    for x in mycursor :
        sector.append(x[0])
        sector_value.append(x[1])
    df  = pd.DataFrame({'sector':sector,'sector_value':sector_value})
#    print (df)
    return df

def cumulative ():
   stock = []
   cumulative_value = []
   mycursor.execute(cred.cumulative_query)
   for x in mycursor :
        stock.append(x[0])
        cumulative_value.append(x[1])
   df  = pd.DataFrame({'stock':stock,'cumulative_value':cumulative_value})
#    print (df)
   return df




def volatile():
   stock = []
   volatile_value = []
   mycursor.execute(cred.volatile_query)
   for x in mycursor :
        stock.append(x[0])
        volatile_value.append(x[1])
   df  = pd.DataFrame({'stock':stock,'Volatile_value':volatile_value})
   return df



def dashboard_page():
 volatile_df = volatile()
 cumulative_df = cumulative()
 sector_df = sector()
 correlation_df = correlation()
 gainer_df = gainer()
 looser_df = looser ()
 st.set_page_config(layout="centered")

 st.title("Nifty-50 Annual Volatile Report")
 fig = px.line(volatile_df,x='stock',y='Volatile_value',labels = {'stock':'stock','Volatile_value':'Volatile_value'})
 st.plotly_chart(fig)

 st.title("Nifty-50 Annual Cumulative Report")
 sig = px.bar(cumulative_df,x='stock',y='cumulative_value',labels = {'stock':'stock','cumulative_value':'cumulative_value'})
 st.plotly_chart(sig)

 st.title("Nifty-50 Annual Sector wise Returns Report")
 self = px.bar(sector_df,x='sector',y='sector_value',labels = {'sector':'sector','sector_value':'sector_value'})
 st.plotly_chart(self)

 st.title("Nifty-50 Highly correlated Stocks")
 corr = px.bar(correlation_df,x='company',y='correlation_value',labels = {'company':'company','correlation_value':'correlation_value'})
 st.plotly_chart(corr)

 st.title("Nifty-50 Top 5 Gainer & Looser Month wise")
 unique_dates = sorted(gainer_df['dates'].unique())
 col1, col2 = st.columns(2)
 for current_date in unique_dates:
    
    df_filtered = gainer_df[gainer_df['dates'] == current_date]
    df_filtered_looser = looser_df[looser_df['dates'] == current_date]

    fig = px.bar(
        df_filtered,
        x='company',
        y='value',
        color='company',
        text='value',
        title=f'Company Value on {current_date}'
    )
    thug = px.bar(
        df_filtered_looser,
        x='company',
        y='value',
        color='company',
        text='value',
        title=f'Company Value on {current_date}'
    )
    with col1:
        st.header("Gainer")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.header("Looser")
        st.plotly_chart(thug, use_container_width=True)

 


 












if __name__ == "__main__":
    dashboard_page()