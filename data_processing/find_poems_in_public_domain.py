from pymongo import MongoClient
import requests
import pandas as pd
import os
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

source_uri = os.environ.get("MONGODB_LOCAL_URI")
# destination_uri = os.environ.get("MONGODB_REMOTE_URI")

api_base_path = "https://api.nb.no/catalog/v1/items/{}?fields=accessInfo&expand=false"


def check_urn(urn_to_check: str) -> bool | dict:
    """Check if a text is free to use.

    Args:
        urn_to_check (str): National library text id (urn) to check

    Returns:
        bool: True if the text is free to use
    """
    response = requests.get(api_base_path.format(urn_to_check))
    if response.status_code == 200:
        return response.json()["accessInfo"]["isPublicDomain"]
    else:
        return {"error": f"Could not find urn {urn_to_check}"}


def main():
    # Connect to the databases
    source = MongoClient(source_uri)
    source_db = source["norn"]

    # Get all urns from the source database
    urns = source_db["poems"].find({}, {"urn": 1, "_id": 0})
    urns_list = [x["urn"] for x in urns]
    urns_list = list(set(urns_list))

    # Check if the urns are public domain
    lst = []
    for urn in tqdm(urns_list):
        res = check_urn(urn)
        lst.append((urn, res))

    df = pd.DataFrame(lst, columns=["urn", "isPublicDomain"])
    not_public = df.loc[df["isPublicDomain"] == False, "urn"].to_list()
    value_counts = df.isPublicDomain.value_counts()
    urns_list = list(set(urns_list))

    # Save the results to a csv file
    df.to_csv("poems_public_domain.csv", index=False)
    
    # Save the urns that are not public domain to a text file
    with open("poem_books_not_in_public_domain.txt", "w") as f:
        for urn in not_public:
            f.write(urn + "\n")

    # Print the results
    print(value_counts)


if __name__ == "__main__":
    main()
