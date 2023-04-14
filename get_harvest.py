import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Cantrak Cannabis Track & Trace")

# Get the ID from the user
id_value = st.text_input("Enter the ID:")

# Call the API with the given ID
if st.button("Submit"):
    url = f"https://ecu-api.avalue.co.th/api/cnb/harvest/{id_value}"
    response = requests.get(url)

    # Display the entire result as JSON on the screen
    if response.status_code == 200:
        data = response.json()
        st.json(data)
    else:
        st.write("Error fetching data from API")
