# text_deduplicator

#### A utility for detecting and labeling duplicate text entries in a pandas DataFrame using TF-IDF and cosine similarity.

### Steps for installation and running code example


```python
!pip install git+https://github.com/MihirAnam/text_deduplication.git
```


```python
import pandas as pd
```


```python
from text_deduplicator import find_duplicates
```


```python
df_dedup = pd.read_excel("output_combined/2024/cyber_2024_cra_combined.xlsx")
```


```python
df_dedup=df_dedup[df_dedup['text']!="-"]
df_dedup.shape
```




    (24486, 13)




```python
df_dedup['text'].isna().sum()
```




    np.int64(2436)




```python
df_dedup=df_dedup[df_dedup['text'].isna()==False]
df_dedup.shape
```




    (22050, 13)




```python
df_dedup.columns
```




    Index(['Date', 'Headline', 'URL', 'Opening Text', 'Source', 'type',
           'hit sentence', 'status', 'title', 'text', 'article_length', 'summary',
           'keywords'],
          dtype='object')




```python
dd=find_duplicates(df_dedup,column='text')
```

    Creating index.
    Creating tfidf vectors
    creating cosine simalarity matrix
    mapping duplicates
    


```python
dd[dd['duplicates'] =="Duplicate"].shape
```




    (6884, 16)




```python
dd=find_duplicates(df_dedup,column='text',consider_date=True,date_column="Date",sub_check=True)
```

    Creating index.
    Creating tfidf vectors
    creating cosine simalarity matrix
    mapping duplicates
    


```python
dd[dd['duplicates'] =="Duplicate"].shape
```




    (7249, 16)




```python
dd=find_duplicates(df_dedup,column='text',threshold=0.70,consider_date=True,date_column="Date",sub_check=True)
```

    Creating index.
    Creating tfidf vectors
    creating cosine simalarity matrix
    threshold set to -  0.7
    mapping duplicates
    


```python
dd[dd['duplicates'] =="Duplicate"].shape
```




    (7931, 16)




```python

```
