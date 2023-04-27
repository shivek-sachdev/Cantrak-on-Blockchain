import streamlit as st
import requests

# Define the API endpoints for each option
ENDPOINTS = {
    "Grow": "https://ecu-api.avalue.co.th/api/cnb/grow/{}",
    "Harvest": "https://ecu-api.avalue.co.th/api/cnb/harvest/{}",
    "Production": "https://ecu-api.avalue.co.th/api/cnb/prod/{}",
    "Sales": "https://ecu-api.avalue.co.th/api/cnb/sales/{}"
}

# Define the options for the radio buttons
OPTIONS = list(ENDPOINTS.keys())

# Create the Streamlit app
st.title("Transaction Data")

# Create radio buttons for the options
option = st.radio("Choose an option", OPTIONS)

# Get the transaction ID from the user
id_value = st.text_input("Enter the transaction ID")

# Call the API based on the user's choice
if st.button("Submit"):
    if id_value:
        endpoint = ENDPOINTS[option].format(id_value)
        response = requests.get(endpoint)

        if response.status_code == 200:
            st.write(response.json())
        else:
            st.write("Error: Could not fetch data.")
    else:
        st.write("Please enter a transaction ID.")
