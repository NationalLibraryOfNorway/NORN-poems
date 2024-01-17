import streamlit as st
import pandas as pd
from pymongo import MongoClient

def display_document(doc_id):
    doc = db.your_collection.find_one({"_id": doc_id})
    return doc['text'] if doc else "Document not found"


# Replace the URI with your actual connection string
client = MongoClient()
db = client.norn

# Add a title
st.title('MongoDB Browser')

# Query MongoDB
documents = list(db.poems.find({}, {"urn" : 1, "title" : 1}))  # Modify as per your collection

# Display data
df = pd.DataFrame(documents)

# st.dataframe(df)
#df['View'] = df['_id'].apply(lambda x: f"[View](#view-{x})")
#st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

for idx, row in df.iterrows():
    # Create a hyperlink for each document
    link = f"[View](#view-{row['_id']})"
    st.write(f"{row['title']} - {link}", unsafe_allow_html=True)


for idx, row in df.iterrows():
    if st.button("View", key=row['_id']):
        st.session_state['selected_doc_id'] = row['_id']

if 'selected_doc_id' in st.session_state:
    st.markdown(f"<a name='view-{st.session_state['selected_doc_id']}'></a>", unsafe_allow_html=True)
    selected_doc_text = display_document(st.session_state['selected_doc_id'])
    st.write(selected_doc_text)
