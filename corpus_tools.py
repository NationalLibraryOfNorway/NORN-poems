from urllib.parse import urljoin
import requests
import pandas as pd
from typing import List
from collections import Counter


def get_poems(api_path = "https://api.nb.no/dhlab/norn") -> pd.DataFrame:
    """Get norn poems

    Args:
        api_path (str, optional): alternative path. Defaults to "https://api.nb.no/dhlab/norn".

    Returns:
        pd.DataFrame: poems
    """
    poem_path = urljoin(api_path, "norn/poems")
    poems = requests.get(poem_path).json()
    return pd.DataFrame(poems)


def get_window(token: str, df: pd.DataFrame, window: int):
    conc = []
    for _, row in df.iterrows():
        if token in row.tokens:
            idxs = [i for i, x in enumerate(row.tokens) if x == token]
            for word_index, idx in enumerate(idxs):
                start = row.tokens[max(0, idx-window):idx]
                end = row.tokens[idx+1:min(len(row.tokens), idx+window+1)]
                
                conc.append({
                    "dhlabid" : row.dhlabid,
                    "concordance_index" : word_index + 1,
                    "word_index" : idx,
                    "left" : start,
                    "token" : token,
                    "right" : end,
                        })
            
            
    return pd.DataFrame(conc)


def concordance(token: str, df: pd.DataFrame, window=5, join=False) -> pd.DataFrame:
    """Get concordance for a token in a dataframe

    Args:
        token (str): target token
        df (pd.DataFrame): target dataframe with tokens
        window (int, optional): number of tokens before and after to check. Defaults to 5.
        join (bool, optional): joined view with html. Defaults to False.

    Returns:
        pd.DataFrame: result dataframe
    """
    res = get_window(token, df, window)
    res.left = res.left.apply(lambda x: " ".join(x))
    res.right = res.right.apply(lambda x: " ".join(x))
    
    if join == True:
        res["concordance"] = res.left + " " + "<b>" + res.token + "</b>" + " " + res.right
        res = res.drop(["left", "token", "right"], axis=1)        
        
    return res



def find_index_distance(lst: List[int]):
    """Find distance between elements in a list

    Args:
        lst (List[str]): list of tokens

    Returns:
        List[int]: distance between tokens
    """
    return [j-i for i, j in zip(lst[:-1], lst[1:])]

def collocation(token, df , window = 10):
    hits = get_window(token, df, window)
    
    counter = Counter()
    
    for _, row in hits.iterrows():

        
        counter.update(row.left)
        counter.update(row.right)
        
    return pd.DataFrame.from_dict(counter, orient="index", columns=["frequency"]).sort_values(by="frequency", ascending=False)
    


def total_word_count(df: pd.DataFrame) -> pd.DataFrame:
    """Get total word count for a dataframe with tokens

    Args:
        df (pd.DataFrame): Dataframe with tokens

    Returns:
        pd.DataFrame: result dataframe
    """
    total = Counter()
    for i, row in df.iterrows():
        total.update(row.tokens)
        
    return pd.DataFrame.from_dict(total, orient="index", columns=["frequency"]).sort_values(by="frequency", ascending=False)


def get_dtm(df: pd.DataFrame) -> pd.DataFrame:
    """Get document term matrix

    Args:
        df (pd.DataFrame): dataframe with text_ids and tokens

    Returns:
        pd.DataFrame: _description_
    """
    dtm = df.tokens.apply(lambda x: pd.Series(Counter(x)))
    return dtm.fillna(0).astype(int)

def count_token(token: str, df: pd.DataFrame) -> int:
    return df.tokens.apply(lambda x: x.count(token)).sum()

def count_tokens(tokens: List[str], df: pd.DataFrame) -> pd.DataFrame:
    """Count list of tokens in a dataframe

    Args:
        tokens (List[str]): list of string tokens
        df (pd.DataFrame): target dataframe

    Returns:
        pd.DataFrame: frequency of tokens
    """
    return pd.DataFrame.from_dict({token: count_token(token, df) for token in tokens}, orient="index", columns=["frequency"]).sort_values(by="frequency", ascending=False)


def relative_collocation(word: str, poems: pd.DataFrame, reference: pd.DataFrame, window = 25) -> pd.DataFrame:
    """Relative concordance for a word in a corpus compared to a reference corpus

    Args:
        word (str): target string
        poems (pd.DataFrame): target texts
        reference (pd.DataFrame): reference texts
        window (int, optional): tokens before and after target. Defaults to 25.

    Returns:
        pd.DataFrame: relative frequency of concordances
    """
    # Hent konkordanser for ordet
    coll = collocation(word, poems, window=window)    
    
    # Regn ut relativ frekvens
    return (coll /reference).sort_values(by="frequency", ascending=False)

def get_reference_corpus(period=(1800,1900)):
    #url = "https://api.nb.no/dhlab/#/default/get_reference_corpus"
    url = "https://api.nb.no/dhlab/reference_corpus"
    from_year = period[0]
    to_year = period[1]
    res = requests.get(url, params={"corpus": "digibok", 'from_year':from_year, 'to_year':to_year, "limit":50000, "lang" : 'nob'})
    #if res.response_code == 200:
    return pd.DataFrame(res.json(), columns=['word', 'frequency']).set_index("word")
    


# 
# dtm  = df.set_index("dhlabid").tokens.explode().reset_index().reset_index().rename({"index" : "frequency"}, axis = 1).groupby(["dhlabid", "tokens"]).count().unstack().fillna(0).astype(int)

# 
# dtm.transpose().droplevel(0)

# 
# dtm.iloc[1].to_frame().head(30).style

# 
# df.set_index("dhlabid").tokens.explode().index.value_counts()

# 
# get_dtm(df)

# 
# total_word_count(df)

# 
# (collocation("havet", df, window=10)  / total_word_count(df)).sort_values(by="frequency", ascending=False).head(20)

# 
# concordance("vikings", df, window=10)

# 
# res = get_window("havet", df, 5)

# res

# 
# res.groupby("dhlabid")["word_index"].count()

# 
# vals = res.groupby("dhlabid")["word_index"].unique()
# vals

# 
# for i, val in vals.items():
#     distances = find_index_distance(val)
#     if distances:
#         for distance in distances:
#             if distance < 10:
#                 print(i, val, distances, distance)
            
            
#         # print(i, find_index_distance(val))

# 


# 
# count_token("havet", df)

# 
# count_tokens(["havet", "skogen"], df)

# 
# collocation("hei", df)

# 
# df.set_index("dhlabid").loc[:, ["text", "tokens"]]

# 
# concordance("havet", df, 20, join = True).head().style


