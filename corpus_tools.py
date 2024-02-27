# %%
from urllib.parse import urljoin
import requests
import pandas as pd

#api_path = "http://dhlab2.nb.no:5004/norn"
api_path = "https://api.nb.no/dhlab/norn"

poem_path = urljoin(api_path, "norn/poems")


poems = requests.get(poem_path).json()

# %%
df = pd.DataFrame(poems)

def get_poems(api_path = "https://api.nb.no/dhlab/norn"):
    poem_path = urljoin(api_path, "norn/poems")
    poems = requests.get(poem_path).json()
    return pd.DataFrame(poems)

# %%
def get_window(token, df, window):
    conc = []
    for _, row in df.iterrows():
        if token in row.tokens:
            #idx = row.tokens.index(token)
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
            
            
            # conc.append(" ".join(row.tokens[idx-window:idx+window+1]))
    return pd.DataFrame(conc)

# %%
def concordance(token, df, window=5, join=False):
    res = get_window(token, df, window)
    res.left = res.left.apply(lambda x: " ".join(x))
    res.right = res.right.apply(lambda x: " ".join(x))
    
    if join == True:
        res["concordance"] = res.left + " " + "<b>" + res.token + "</b>" + " " + res.right
        res = res.drop(["left", "token", "right"], axis=1)        
        
    return res

# %%
from typing import List
from collections import Counter

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
    

# %%
def total_word_count(df):
    total = Counter()
    for i, row in df.iterrows():
        total.update(row.tokens)
        
    return pd.DataFrame.from_dict(total, orient="index", columns=["frequency"]).sort_values(by="frequency", ascending=False)

# %%
def get_dtm(df):
    dtm = df.tokens.apply(lambda x: pd.Series(Counter(x)))
    return dtm.fillna(0).astype(int)

def count_token(token, df):
    return df.tokens.apply(lambda x: x.count(token)).sum()

def count_tokens(tokens, df):
    # return df.tokens.apply(lambda x: sum([x.count(token) for token in tokens])).sum()
    return pd.DataFrame.from_dict({token: count_token(token, df) for token in tokens}, orient="index", columns=["frequency"]).sort_values(by="frequency", ascending=False)


# # %%
# dtm  = df.set_index("dhlabid").tokens.explode().reset_index().reset_index().rename({"index" : "frequency"}, axis = 1).groupby(["dhlabid", "tokens"]).count().unstack().fillna(0).astype(int)

# # %%
# dtm.transpose().droplevel(0)

# # %%
# dtm.iloc[1].to_frame().head(30).style

# # %%
# df.set_index("dhlabid").tokens.explode().index.value_counts()

# # %%
# get_dtm(df)

# # %%
# total_word_count(df)

# # %%
# (collocation("havet", df, window=10)  / total_word_count(df)).sort_values(by="frequency", ascending=False).head(20)

# # %%
# concordance("vikings", df, window=10)

# # %%
# res = get_window("havet", df, 5)

# res

# # %%
# res.groupby("dhlabid")["word_index"].count()

# # %%
# vals = res.groupby("dhlabid")["word_index"].unique()
# vals

# # %%
# for i, val in vals.items():
#     distances = find_index_distance(val)
#     if distances:
#         for distance in distances:
#             if distance < 10:
#                 print(i, val, distances, distance)
            
            
#         # print(i, find_index_distance(val))

# # %%


# # %%
# count_token("havet", df)

# # %%
# count_tokens(["havet", "skogen"], df)

# # %%
# collocation("hei", df)

# # %%
# df.set_index("dhlabid").loc[:, ["text", "tokens"]]

# # %%
# concordance("havet", df, 20, join = True).head().style


