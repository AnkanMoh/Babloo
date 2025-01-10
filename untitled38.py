# -*- coding: utf-8 -*-
"""Untitled38.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_aVgUZOu4gPLV8BzCQf6OeW75xDrXbdx
"""

import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROK_API_URL = "https://api.groq.com/query"  # Replace with the actual endpoint
API_KEY = os.getenv("GROK_API_KEY")  # Retrieve the API key securely
GROK_API_KEY='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'

st.title("Bablu - Salon Data Chatbot")
st.write("Upload your salon data in Excel format and ask Bablu your questions!")

# File Upload Section
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Global variable to hold the data
df = None

if uploaded_file:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("**Uploaded Data:**")
    st.dataframe(df)

# Query Input Section
user_query = st.text_input("Ask Bablu a question:")

if st.button("Ask Bablu"):
    if df is not None and user_query.strip():
        # Convert the uploaded data to JSON format for the Grok API
        data_json = df.to_dict(orient="records")

        # Prepare the payload for the Grok API
        payload = {
            "data": data_json,  # Salon data in JSON format
            "query": user_query  # User's natural language query
        }

        # Prepare headers with the API key
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        try:
            # Make a POST request to the Grok API
            response = requests.post(GROK_API_URL, json=payload, headers=headers)

            # Handle the API response
            if response.status_code == 200:
                result = response.json()
                st.success(f"Bablu says: {result.get('response', 'No response received')}")
            else:
                st.error(f"Error: Received status code {response.status_code} from Grok API.")
        except Exception as e:
            st.error(f"An error occurred while communicating with the Grok API: {e}")
    else:
        st.warning("Please upload an Excel file and enter a query!")
else:
    st.info("Bablu is waiting for your query!")