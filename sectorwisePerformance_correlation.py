import pandas as pd
from pathlib import Path
import numpy as np
folder_path = Path("Visuvalization_excels")

rootPath = Path("CSV")

# df['date'] = pd.to_datetime(df['date'])
# df = df.sort_values(['Ticker', 'date']).reset_index(drop=True)

def overalldataframe () :
    df  = pd.DataFrame()
    wholedf = pd.DataFrame()
    for file in rootPath.iterdir():
        wholedf = pd.read_csv(f"CSV/{file.name}")
        df = pd.concat([df,wholedf], ignore_index=True)
    print(df)
    return df



def correlation () :
    df = overalldataframe()
    df['Daily_Return'] = df.groupby('Ticker')['close'].pct_change()
    returns_df = df.pivot(index='date', columns='Ticker', values='Daily_Return')
    correlation_matrix = returns_df.corr()
    # 1. Unstack the correlation matrix (convert it from a grid to a list of pairs)
    correlation_series = correlation_matrix.unstack()
    processed_pairs = set()
    
    def is_unique_pair(index):
        # The index is a tuple: (Ticker_1, Ticker_2)
        ticker1, ticker2 = index
        # Filter out self-correlations
        if ticker1 == ticker2:
            return False
        # Create a "canonical" representation of the pair (sorted tuple)
        # This ensures (A, B) and (B, A) are treated as the same
        canonical_pair = tuple(sorted((ticker1, ticker2)))
        
        if canonical_pair not in processed_pairs:
            processed_pairs.add(canonical_pair)
            return True
        return False

    # Apply the filter function to the index
    unique_correlation_series = correlation_series[correlation_series.index.map(is_unique_pair)]

    # 3. Sort by correlation value (absolute value for strongest correlation, or just descending for most positive)
    # Here, we sort descending to find the highest *positive* correlations first.
    # Use .abs().sort_values(ascending=False) for the strongest correlation (positive or negative).
    top_10_correlations = unique_correlation_series.sort_values(ascending=False).head(10)
    
    
    # --- Print and Output ---
    
    print("\n" + "="*50)
    print("      Top 10 Company Pairs and Their Correlation")
    print("="*50)
    print(top_10_correlations.to_string())
    print("="*50)
    # print("Correlation Matrix of Daily Returns:")
    # print(correlation_matrix.to_markdown(floatfmt=".4f"))
    file_path = folder_path / "corelation_Metrix_top10.xlsx"
    top_10_correlations.to_excel(file_path, index=False)

def sector_wise_performance () :
    df = overalldataframe()
    ticker_stats = df.groupby('Ticker').agg(
        first_price=('close', 'first'),
        last_price=('close', 'last'),
        N=('close', 'count'),  # Number of trading days in the period
        sector=('sector', 'first') # Get the sector name
    ).reset_index()

    ticker_stats['Cumulative_Return'] = (ticker_stats['last_price'] / ticker_stats['first_price']) - 1

    TRADING_DAYS_PER_YEAR = 252
    ticker_stats['Annualized_Return'] = (
        (1 + ticker_stats['Cumulative_Return']) ** (TRADING_DAYS_PER_YEAR / ticker_stats['N']) - 1
    )


    sector_returns = ticker_stats.groupby('sector')['Annualized_Return'].mean().reset_index()

    sector_returns.rename(
        columns={'Annualized_Return': 'Average_Yearly_Return'},
        inplace=True
    )
    sector_returns['Average_Yearly_Return_Percent'] = sector_returns['Average_Yearly_Return'] * 100

    print(sector_returns)

    file_path = folder_path / "sector_wise_performance.xlsx"
    sector_returns.to_excel(file_path, index=False)

# print(sector_returns[['sector', 'Average_Yearly_Return_Percent']].to_markdown(index=False, floatfmt=".2f"))

# sector_wise_performance()
correlation()
# gainerLooser()
