import requests
import streamlit as st

# Set the API endpoint URL
url = "https://api.owlracle.info/v4/poly/gas"

# Set the request parameters
params = {"apikey": "9b2a10bb73d24c22ba0bde52134a0419", "blocks": 200, "accept": 100}

# Call the API endpoint
response = requests.get(url, params=params)

# Check if the response is successful
if response.status_code == 200:
    # Extract the "estimatedFee" field from the first item in the "speeds" array
    data = response.json()
    speeds = data["speeds"]
    estimated_fee = speeds[0]["estimatedFee"]
    
    # Display the "estimatedFee" field on the screen using st.metric
    st.metric(label="Estimated Gas Fee", value=f"${estimated_fee:.2f}")
    
    # Display the rest of the response as JSON
    #st.write("Full response:")
    #st.json(data)
else:
    # If the response is not successful, display an error message
    st.error(f"Error: {response.status_code} - {response.reason}")
