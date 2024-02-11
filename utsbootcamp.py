import numpy as np
import datetime as dt

import pandas as pd
import yfinance as yf

import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup
from IPython.display import display, Math, Latex

def PageBreakPDF():
	# from IPython.display import display, Math, Latex
	# Usage: bc.PageBreakPDF()
	# Adds a page break in PDF output when saving Jupyter Notebook to PDF via LaTeX
	display(Latex(r"\newpage"))

def my_function():
    print('Hello you.')
	
def my_function2(name):
    print(f"Hello {name}, is it me you're looking for?")

def my_function3(name):
    print(f"Hello {name.capitalize()}, is it me you're looking for?")

def my_function4(name='alex'):
    if isinstance(name,str):
        print(f"Hello {name.capitalize()}, is it me you're looking for?")
    else:
        print('Inputs must be strings')	

def price2ret(x):
	ret = x.pct_change()
	return ret
	
def price2cret(x):
	ret = x.pct_change()
	cret=((1 + ret).cumprod() - 1)
	return cret

def get_yahoo_data(ticker_list,
          start=dt.datetime(2020, 1, 2),
          end=dt.datetime(2020, 4, 30),
          column='Adj Close',plot=False):
    """
    This function reads in market data from Yahoo
    for each ticker in the ticker_list.
    
    Parameters
    ----------
    ticker_list : dict
        Example ticker_list = {'INTC': 'Intel',
               'MSFT': 'Microsoft',
               'IBM': 'IBM',
               'BHP': 'BHP',
               'TM': 'Toyota',
               'AAPL': 'Apple',
               'AMZN': 'Amazon',
               'BA': 'Boeing',
               'QCOM': 'Qualcomm',
               'KO': 'Coca-Cola',
               'GOOG': 'Google',
               'SNE': 'Sony',
               'PTR': 'PetroChina'}
    
    start : datetime, str ['yyyy-mm-dd'] 
    
    end : datetime, str ['yyyy-mm-dd']
    
    column : str ['Open', 'Low', 'High', 'Close',
        'Adj Close' (default), 'Volume']

    Returns
    -------
    pd.DataFrame
        Pandas dataframe containing specified columns for all tickers requested
    """
    
    ticker = pd.DataFrame()

    for tick in ticker_list:
        prices = yf.download(tick, start, end)
        closing_prices = prices[column]
        ticker[tick] = closing_prices
    
    if plot:
        ret = ticker.pct_change()
        ((1 + ret).cumprod() - 1).plot(title='Cumulative Returns',figsize=(12,8))
    
    return ticker




class HTMLTableParser:
       
        def parse_url(self, url):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            return [(table['id'],self.parse_html_table(table))\
                    for table in soup.find_all('table')]  
    
        def parse_html_table(self, table):
            n_columns = 0
            n_rows=0
            column_names = []
    
            # Find number of rows and columns
            # we also find the column titles if we can
            for row in table.find_all('tr'):
                
                # Determine the number of rows in the table
                td_tags = row.find_all('td')
                if len(td_tags) > 0:
                    n_rows+=1
                    if n_columns == 0:
                        # Set the number of columns for our table
                        n_columns = len(td_tags)
                        
                # Handle column names if we find them
                th_tags = row.find_all('th') 
                if len(th_tags) > 0 and len(column_names) == 0:
                    for th in th_tags:
                        column_names.append(th.get_text())
    
            # Safeguard on Column Titles
            if len(column_names) > 0 and len(column_names) != n_columns:
                raise Exception("Column titles do not match the number of columns")
    
            columns = column_names if len(column_names) > 0 else range(0,n_columns)
            df = pd.DataFrame(columns = columns,
                              index= range(0,n_rows))
            row_marker = 0
            for row in table.find_all('tr'):
                column_marker = 0
                columns = row.find_all('td')
                for column in columns:
                    df.iat[row_marker,column_marker] = column.get_text()
                    column_marker += 1
                if len(columns) > 0:
                    row_marker += 1
                    
            # Convert to float if possible
            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass
            
            return df