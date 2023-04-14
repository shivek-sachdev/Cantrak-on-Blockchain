import requests
import streamlit as st

# Set the API endpoint URLs
poly_url = "https://api.owlracle.info/v4/poly/gas"
eth_url = "https://api.owlracle.info/v4/eth/gas"

# Set the request parameters
params = {"apikey": "8cc9f667b99e499ba630a95cac6bd25c", "blocks": 200, "accept": 100}

# Call the poly endpoint
poly_response = requests.get(poly_url, params=params)

# Check if the poly response is successful
if poly_response.status_code == 200:
    # Extract the "estimatedFee" field from the first item in the "speeds" array
    poly_data = poly_response.json()
    poly_speeds = poly_data["speeds"]
    poly_estimated_fee = poly_speeds[0]["estimatedFee"]
else:
    # If the response is not successful, display an error message
    st.error(f"Poly Error: {poly_response.status_code} - {poly_response.reason}")
    poly_estimated_fee = None

# Call the eth endpoint
eth_response = requests.get(eth_url, params=params)

# Check if the eth response is successful
if eth_response.status_code == 200:
    # Extract the "estimatedFee" field from the first item in the "speeds" array
    eth_data = eth_response.json()
    eth_speeds = eth_data["speeds"]
    eth_estimated_fee = eth_speeds[0]["estimatedFee"]
else:
    # If the response is not successful, display an error message
    st.error(f"ETH Error: {eth_response.status_code} - {eth_response.reason}")
    eth_estimated_fee = None

# Calculate the percentage difference between the estimated gas fees for Poly and Eth
if poly_estimated_fee is not None and eth_estimated_fee is not None:
    difference_percent = (eth_estimated_fee - poly_estimated_fee) / eth_estimated_fee * 100
else:
    difference_percent = None

# Create two columns to display the metrics
col1, col2 = st.columns(2)

# Display the "estimatedFee" field for poly on the screen using st.metric
with col1:
    if poly_estimated_fee is not None:
        # Display the "estimatedFee" field for poly on the screen using st.metric
        st.metric(label="Poly Estimated Gas Fee", value=f"${poly_estimated_fee:.3f}")
        if difference_percent is not None:
            # Display the percentage difference between the estimated gas fees for Poly and Eth
            st.write(f"Poly is {difference_percent:.2f}% cheaper than ETH")
    else:
        st.write("Poly gas fee not available")

with col2:
    if eth_estimated_fee is not None:
        # Display the "estimatedFee" field for eth on the screen using st.metric
        st.metric(label="ETH Estimated Gas Fee", value=f"${eth_estimated_fee:.3f}")
    else:
        st.write("ETH gas fee not available")
