#!/usr/bin/env python
# coding: utf-8

# # Apply LDA to the paragraph set to identify candidate topics

# ## Data wrangling
# ### Clean up paragraph text data. Remove punctuation; lowercase the text.

# In[1]:


import pandas as pd
import string

# data wrangling/cleaning
paragraphs_df = pd.read_csv('election_paragraphs.csv', delimiter = '///', engine = 'python')

# remove punctuation
paragraphs_df['Paragraph'] = paragraphs_df['Paragraph'].apply(lambda x: ''.join([c for c in x if c not in string.punctuation]))

# lowercase paragraph text
paragraphs_df = paragraphs_df.apply(lambda x: x.str.lower())


# ### Results

# In[2]:


paragraphs_df


# ### Vectorizing the text

# In[3]:


import pandas as pd

# helper function: returns the k most frequently appearing keywords in the dataframe
def top_k(data_df, vec, k):
    X = vec.fit_transform(data_df['Paragraph'].values)
    labels = vec.get_feature_names()
    
    return pd.DataFrame(columns = labels, data = X.toarray()).sum().sort_values(ascending = False)[:k]


# In[4]:


## generate feature vectors
from sklearn.feature_extraction.text import CountVectorizer 

vec = CountVectorizer(decode_error = 'ignore', stop_words = 'english')
X = vec.fit_transform(paragraphs_df['Paragraph'].values)


# #### Most frequent terms over all paragraphs

# In[5]:


top_terms = top_k(paragraphs_df, vec, 30)

top_terms


# ## Topic modeling with LDA

# In[6]:


# helper function: prints the top k candidate topics
def print_topics(topic_model, vec, k):
    terms = vec.get_feature_names()
    for topic_idx, topic in enumerate(topic_model.components_):
        print("Topic #%d:" %topic_idx)
        print(" ".join([terms[i] for i in topic.argsort()[:-k - 1:-1]]) + '\n')


# In[7]:


from sklearn.decomposition import LatentDirichletAllocation as LDA

tn = 30
lda = LDA(n_components = tn)
lda.fit(X)


# ### Candidate topics

# In[8]:


print_topics(lda, vec, 10)


# In[9]:


# transform document word matrix according to the fitted LDA model
document_topic_distribution = lda.transform(X)
document_topic_df = pd.DataFrame(document_topic_distribution)
document_topic_df['Date'] = paragraphs_df['Date']

topic_coverage = document_topic_df.groupby(['Date']).agg({i: 'sum' for i in range(30)})


# ### Topic coverage results

# In[10]:


topic_coverage


# In[11]:


import matplotlib.pyplot as plt

plt.plot(topic_coverage)
plt.ylabel('Coverage')
plt.xlabel('Date')
plt.show()

