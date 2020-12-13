#!/usr/bin/env python
# coding: utf-8

# # Granger testing

# In[ ]:


from statsmodels.tsa.stattools import grangercausalitytests as gct

lag = 3
granger_test_results = list()
for i in range(0, len(election_prices_topics.columns) - 1):
    result = gct(election_prices_topics[['NormalizedPrice', i]], maxlag = lag, verbose = True)
    granger_test_results.append(result)


# # Significant causal words

# ## Compute average p-values across time lags

# In[ ]:


p_values = dict()

for i in range(len(granger_test_results)):
    p_value = 0
    for j in range(1, lag):
        p_value += granger_test_results[i][j][0]['params_ftest'][1]
    p_value /= lag
    p_values[i] = p_value
                
p_values


# ## Terms sorted by causality probability

# In[ ]:


p_values = dict(sorted(p_values.items(), key = lambda entry: entry[1]))

p_values


# # Prior influence

# ## Positive impact terms

# In[ ]:


list(p_values)[:15]


# ## Negative impact terms

# In[ ]:


list(p_values)[15:]


# # Visualization

# In[ ]:


from wordcloud import WordCloud

all_paragraphs = ' '.join(list(paragraphs_df['Paragraph'].values))
wordcloud = WordCloud(max_words = 300)
wordcloud.generate(all_paragraphs)
wordcloud.to_image()

