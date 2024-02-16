"""Process names in poems database

This script processes the names in the poems database. It switches the names from the format "Last, First" to "First Last". It also handles cases where the name is a list of names separated by a slash. In these cases, the names are separated by a slash in the output as well.
"""

# %%
from pymongo import MongoClient
import os
import pandas as pd

# Connect to the database
uri = os.environ.get('MONGODB_LOCAL_URI') 

client = MongoClient(uri)
db = client['norn']
poems = db['poems']

# %%
names = [poem["author"] for poem in poems.find()]
df = pd.DataFrame(names, columns=["author"])

# %%
def parse_name(name):
    last_name, first_name = name.split(',')
    last_name = last_name.strip()
    first_name = first_name.strip()
    return f"{first_name} {last_name}"

def parse_multiname(name):
    names = name.split('/')
    names = [parse_name(name) for name in names]
    return " / ".join(names)

def switch_names(name):
    if "," in name:
        if "[" in name:
            return name        
        elif "/" in name:
            return parse_multiname(name)
        else:
            return parse_name(name)
    else:
        return name
    

# %%
test_cases = [
    "[gymnasialsamfundet \"Fram\"]",
    "Jacob B. Bull / A. Bloch",
    "J.L. (Johannes Lockert) Pedersen",
    "Berg, Olaf [Martin Kvænnavika]",
    "Edith [Sigurdsen, Sofie]",
    "Theodor Caspari / Theodor Kittelsen"
    
]

switched_names = [switch_names(name) for name in names]
sw_n_df = pd.DataFrame(switched_names)
for case in test_cases:
    assert switch_names(case) == case

# %%
for poem in poems.find():
    poem["author"] = switch_names(poem["author"])
    poems.update_one({"_id": poem["_id"]}, {"$set": {"author": poem["author"]}})
    


