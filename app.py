import streamlit as st
import requests
import json
import pandas as pd
from databricks import sql

def get_query(question):
    url = 'https://dbc-164e54c4-ef63.cloud.databricks.com/serving-endpoints/Final_Testing/invocations'
    headers = {'Authorization': f'Bearer {"dapi7aff94b92948d811e9f9019293f4705d"}', 'Content-Type': 'application/json'}
    data_json = {'inputs': [question]}
    response = requests.request(method='POST', headers=headers, url=url, data=json.dumps(data_json))
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()

def run_query(sql_query):
    connection = sql.connect(
        server_hostname="dbc-164e54c4-ef63.cloud.databricks.com",
        http_path="/sql/1.0/warehouses/591de624a7eca260",  
        access_token="dapi7aff94b92948d811e9f9019293f4705d"
    )
    cursor = connection.cursor()
    cursor.execute(sql_query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(data, columns=columns)

st.title("Demo: Databricks model from Streamlit")
user_input = st.text_input("Ask your question")
if st.button("Send"):
    try:
        result = get_query(user_input)
        sql_query = result['predictions'][0]['sql']
        #data = run_query(sql_query)
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language='sql')
        st.json(result)
        st.subheader("Query Result:")
        #st.dataframe(data)
    except Exception as e:
        st.error(f"Error: {e}")
