import requests
import streamlit as st

st.title("Retrieve Data from API by ID")

id = st.text_input("Enter the ID:")

if st.button("Submit"):
    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        url = f"https://ecu-api.avalue.co.th/api/cnb/harvest/{id}"
        response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Success! hashId: {result['hashId']}")
        st.success(f"Validate your transaction here: {result['explorerURL']}")
    else:
        st.error("Error: Unable to retrieve data from the API.")
