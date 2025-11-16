import streamlit as st
import requests
import json

# Config
DATABRICKS_URL = "https://<workspace-url>/serving-endpoints/<nombre-endpoint>/invocations"
TOKEN = "<TU_TOKEN_DATABRICKS>"

st.title("Demo: Databricks model from Streamlit")

user_input = st.text_input("Ask your question")

if st.button("Send"):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "dataframe_records": [{"text": user_input}]
    }

    response = requests.post(DATABRICKS_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        st.write("Result:", result)
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)
