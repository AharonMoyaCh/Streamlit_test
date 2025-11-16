import streamlit as st
import requests
import json

# Config
DATABRICKS_URL = "https://dbc-164e54c4-ef63.cloud.databricks.com/serving-endpoints/Final_Testing/invocations"
TOKEN = "dapi7aff94b92948d811e9f9019293f4705d"

st.title("Demo: Databricks model from Streamlit")

user_input = st.text_input("Ask your question")
if st.button("Send"):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "input": [user_input]
    }

    response = requests.post(DATABRICKS_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        st.write("Result:", result)
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)
