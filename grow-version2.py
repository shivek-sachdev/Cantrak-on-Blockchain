import streamlit as st
import pandas as pd
import requests
import time

# Load data from CSV file
data = pd.read_csv("Cantrak-on-Blockchain\cantrak_data.csv", encoding="TIS-620")

# Set page title and add image
st.set_page_config(page_title="Cantrak on Polygon Blockchain", page_icon=":herb:")

# Define the input form for the user to select a Transaction ID
# First part - Cultivation Data
st.header("Cultivation Data")
selected_id = st.selectbox("Transaction ID", data["Transaction ID"])

# Get the row corresponding to the selected Transaction ID
selected_row = data.loc[data["Transaction ID"] == selected_id].iloc[0]

# Display the rest of the data for the selected Transaction ID
name = st.text_input("Plant Lot Name", selected_row["Plant Lot Name"])
lotNo = st.text_input("Plant Lot Number", selected_row["Plant Lot Number"])

with st.expander("Cultivation Details"):
    plantLocationName = st.text_input("Growing Location", selected_row["Growing Location"])
    plantSubLocationName = st.text_input("Sub Growing Location", selected_row["Sub Growing Location"])
    plantId = st.text_input("Total Planted", selected_row["Total Planted"])
    plantGrowthStageName = st.text_input("Growth Stage", selected_row["Growth Stage"])
    itemId = st.text_input("Item Used for Growing", selected_row["Item Used for Growing"])
    itemLotNo = st.text_input("Item Lot Number", selected_row["Item Lot Number"])

# Second part - Transaction Details (expandable box)
with st.expander("Additional Details"):
    companyId = st.text_input("Company Name", selected_row["Company Name"])
    licenseId = st.text_input("Cultivation License Number", selected_row["Cultivation License Number"])
    createdAt = st.text_input("Created Date", selected_row["Created Date"])
    createdBy = st.text_input("Created By", selected_row["Created By"])
    isActive = st.text_input("Status", selected_row["Status"])

# Set the API endpoint URLs
poly_url = "https://api.owlracle.info/v4/poly/gas"
eth_url = "https://api.owlracle.info/v4/eth/gas"

# Set the request parameters
params = {"apikey": "37468d9a4df84c0797dabe964545f491", "blocks": 200, "accept": 100}

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

# Define the submit button
if st.button("Submit"):
    # Define the request payload
    payload = {
        "id": selected_id,
        "name": name,
        "lotNo": lotNo,
        "plantLocationName": plantLocationName,
        "plantSubLocationName": plantSubLocationName,
        "plantId": plantId,
        "plantGrowthStageName": plantGrowthStageName,
        "itemId": itemId,
        "itemLotNo": itemLotNo,
        "companyId": companyId,
        "licenseId": licenseId,
        "createdAt": createdAt,
        "createdBy": createdBy,
        "isActive": isActive
    }

    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        start_time = time.time() # start the timer
        response = requests.post("https://ecu-api.avalue.co.th/api/cnb/grow", json=payload)
        end_time = time.time() # stop the timer

    if response.status_code == 200:
        result = response.json()
        st.success(f"Success! isCreate: {result['isCreate']}, hashId: {result['hashId']}")
        
        # Update dashboard
        num_transactions = st.session_state.get("num_transactions", 0)
        num_transactions += 1
        st.session_state.num_transactions = num_transactions

        # Update time elapsed metric
        time_elapsed = st.session_state.get("time_elapsed", 0)
        time_elapsed += end_time - start_time
        st.session_state.time_elapsed = time_elapsed

        #call Get Harvest API to display URL
        url = f"https://ecu-api.avalue.co.th/api/cnb/grow/{selected_id}"
        response = requests.get(url)

        # Display only the explorerURL from the JSON response
        if response.status_code == 200:
            data = response.json()
            if 'explorerURL' in data:
                st.write(f"Explorer URL: {data['explorerURL']}")
            else:
                st.write("Explorer URL not found in response.")
    else:
        st.error("Error: Unable to write data onto the Blockchain.")

# Define dashboard
st.sidebar.header("Blockchain Metrics")
num_transactions = st.session_state.get("num_transactions", 0)
st.sidebar.subheader("Number of Transactions")
st.sidebar.write(num_transactions)

time_elapsed = st.session_state.get("time_elapsed", 0)
st.sidebar.subheader("Time Elapsed")
st.sidebar.write(f"{time_elapsed:.2f} seconds")