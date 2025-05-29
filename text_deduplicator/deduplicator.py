import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.metrics import pairwise_distances
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import Binarizer

def merge_lists(lists):
    """
    Merges a list of lists into groups of overlapping elements.

    This function is useful for deduplication tasks where items (e.g., text entries)
    may appear in multiple groups and transitive overlap needs to be resolved.
    It performs a two-pass merge:
    1. Groups lists with direct overlaps.
    2. Merges any indirectly connected groups to ensure transitive connectivity.

    Parameters:
    -----------
    lists : list of list
        A list containing sublists of items (e.g., indices of similar entries) 
        that are candidates for merging.

    Returns:
    --------
    list of list
        A list of merged groups, each represented as a sorted list with no overlaps 
        between groups.
    """

    result = []

    for lst in lists:
        current_set = set(lst)
        merged = False

        # Check for overlaps with existing groups
        for group in result:
            if current_set & group:  # if there's any common element
                group.update(current_set)
                merged = True
                break

        if not merged:
            result.append(current_set)

    # Second pass to merge indirectly connected sets
    i = 0
    while i < len(result):
        j = i + 1
        while j < len(result):
            if result[i] & result[j]:  # if they have common elements
                result[i].update(result[j])
                del result[j]  # remove and merge
            else:
                j += 1
        i += 1

    # Convert to sorted lists
    return [sorted(group) for group in result]

# # Example input
# lists = [[1,2,3], [2,5,6], [89,98,7], [6,8,9]]
# result = merge_lists(lists)
# print(result)


def find_duplicates(df,column,threshold=0.8,consider_date=False,sub_check=False):
    """
    Identifies duplicate text entries in a DataFrame based on cosine similarity using TF-IDF.

    This function detects near-duplicate text entries by computing pairwise cosine 
    similarity on the TF-IDF vectors of the `text` column in the DataFrame.
    It groups similar entries and optionally uses date information to keep 
    the latest record among duplicates.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame containing text entries and optionally a 'Date' column.
        
    column : str
        The name of the column containing the text to check for duplicates.
    
    threshold : float, optional (default=0.8)
        The cosine similarity threshold above which two entries are considered duplicates.
    
    consider_date : bool, optional (default=False)
        If True, keeps the most recent entry (based on 'Date') among duplicates.
        If False, the first entry in each duplicate group is considered the original.
    
    sub_check: bool, optional (default=False)
        If True, Merges any indirectly connected groups to ensure transitive connectivity.
        If False, Returns duplicates within the threshold only, Does not check for sub-groups.
        for eg: if the text1 is duplicate with text2 wrt threshold, and text2 is duplicate with text3 wrt to its threshold, but text1 and text3 are not duplicate directly but inderictly they have same connection.
        So here we can 
    
    Returns:
    --------
    pandas.DataFrame
        A modified version of the input DataFrame with two additional columns:
        - 'duplicates': marks entries identified as duplicates.
        - 'duplicate_with_id': indicates the index of the original (non-duplicate) entry.

    Notes:
    ------
    - Assumes the DataFrame has a 'text' column and an 'index' column set or available.
    - Requires the 'Date' column to be present and parseable if `consider_date` is True.
    - Uses `merge_lists` to ensure transitive closure in duplicate groupings.
    """
    
    print("Creating index.")
    df_dedup=df.reset_index()
    print("Creating tfidf vectors")
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_dedup[column])
    print("creating cosine simalarity matrix")
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=df_dedup['index'], columns=df_dedup['index'])

    print("mapping duplicates")
    l1=[]
    index_list=[]
    for i in similarity_df.columns:
        if i not in l1:
            index=similarity_df[(similarity_df[i]>0.75) & (similarity_df.index!=i)].index
            if len(index)>0:
                l1=l1+list(index)
                # print(">>",i)
                # print(index)
                # print("_"*60)
                index_list.append([i]+list(index))
    
    
    
    index_list2=index_list.copy()
    if sub_check==True:
        index_list3 = merge_lists(index_list2)
    else:
        index_list3=index_list2.copy()
    
    
    if consider_date==False:
        df_dedup['duplicate_with_id']=""
        df_dedup['duplicates']=""
        
        for i in index_list3:
            # print(i)
            # print(i[0])
            dup_index=i[0]
            i.remove(i[0])
            # print(i)
            # print("_"*100)
            df_dedup.loc[df_dedup['index'].isin(i),'duplicates']="Duplicate"
            df_dedup.loc[df_dedup['index'].isin(i),'duplicate_with_id']=dup_index
            
    else:
        df_dedup['duplicate_with_id']=""
        df_dedup['duplicates']=""
        l2=[]
        for i in index_list3:
            # print(i)
            dup_index=df_dedup[df_dedup['index'].isin(i)].sort_values("Date",ascending=False).reset_index(drop=True)[:1]['index'].item()
            # print(dup_index)
            i.remove(dup_index)
            # print(i)
            # print("_"*100)
            l2+=i
            df_dedup.loc[df_dedup['index'].isin(i),'duplicates']="Duplicate"
            df_dedup.loc[df_dedup['index'].isin(i),'duplicate_with_id']=dup_index
        
    return df_dedup
    