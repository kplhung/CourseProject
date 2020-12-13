#!/usr/bin/env python
# coding: utf-8

# # Iowa Electronic Markets (IEM) 2000 Presidential Winner-Takes-All Market

# ## Data wrangling

# In[1]:


import datetime 

# helper function to standardize date formatting between datasets
def format_date(date):
    return datetime.datetime.strptime(date, '%m/%d/%y').strftime('20%y-%m-%d')


# In[2]:


import pandas as pd

iem_prices_df = pd.read_csv('iem_2000.txt', delimiter = '\t')
iem_prices_df = iem_prices_df.drop(['    Units', '    $Volume', '    LowPrice', '    HighPrice', '    AvgPrice'], axis = 1)
iem_prices_df['Date'] = iem_prices_df['Date'].apply(lambda x: format_date(x))
iem_prices_df = iem_prices_df.set_index('Date')


# ### Democratic candidate prices 

# In[3]:


dem_prices_df = iem_prices_df[iem_prices_df['    Contract'].str.contains('Dem')]
dem_prices_df


# ### Republican candidate prices

# In[4]:


rep_prices_df = iem_prices_df[iem_prices_df['    Contract'].str.contains('Rep')]
rep_prices_df


# In[5]:


dem_normalized_prices = dem_prices_df['    LastPrice'] / (dem_prices_df['    LastPrice'] + rep_prices_df['    LastPrice'])
dem_normalized_prices_df = dem_normalized_prices.to_frame()
dem_normalized_prices_df = dem_normalized_prices_df.rename(columns = {'    LastPrice': 'NormalizedPrice'})
dem_normalized_prices_df


# ## Election coverage vs. election forecast

# In[ ]:


election_prices_topics = pd.concat([dem_normalized_prices_df, topic_coverage], axis = 1, join = 'inner')

election_prices_topics

