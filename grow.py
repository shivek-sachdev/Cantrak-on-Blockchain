import streamlit as st
import requests


st.sidebar.title("Menu")
st.sidebar.markdown("[Grow](https://www.wikipedia.com)")
st.sidebar.markdown("[Harvest](https://www.google.com)")
st.sidebar.markdown("[Production](https://www.yahoo.com)")

# Set page title and add image
st.title("Cantrak on Polygon Blockchain")
st.image("https://media.istockphoto.com/id/828088276/vector/qr-code-illustration.jpg", width=200)

# Define the input form for the user to enter data
st.header("Enter the following details:")
id = st.text_input("ID", "222")
name = st.text_input("Name", "test delete harvest2")
createdAt = st.text_input("Created At", "1674702006858")
itemId = st.text_input("Item ID", "25")
itemLotNo = st.text_input("Item Lot No", "5165120001")
licenseId = st.text_input("License ID", "")
lotNo = st.text_input("Lot No", "5266010008")
orgId = st.text_input("Org ID", "203")
plantCurrentLocationId = st.text_input("Plant Current Location ID", "34")
plantCurrentSubLocationId = st.text_input("Plant Current Sub Location ID", "36")
plantGrowthStageName = st.selectbox("Plant Growth Stage Name", ("Vegetative", "Flowering", "Harvest"))
plantLocationName = st.text_input("Plant Location Name", "CHF Greenhouse #2")
plantSerial = st.text_input("Plant Serial", "001-23-01-001219")
plantSubLocationName = st.text_input("Plant Sub Location Name", "แปลง L1")

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


# Define the submit button
if st.button("Submit"):
    # Define the request payload
    payload = {
        "id": id,
        "name": name,
        "createdAt": createdAt,
        "itemId": itemId,
        "itemLotNo": itemLotNo,
        "licenseId": licenseId,
        "lotNo": lotNo,
        "orgId": orgId,
        "plantCurrentLocationId": plantCurrentLocationId,
        "plantCurrentSubLocationId": plantCurrentSubLocationId,
        "plantGrowthStageName": plantGrowthStageName,
        "plantLocationName": plantLocationName,
        "plantSerial": plantSerial,
        "plantSubLocationName": plantSubLocationName
    }

    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        response = requests.post("https://ecu-api.avalue.co.th/api/cnb/grow", json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Success! isCreate: {result['isCreate']}, hashId: {result['hashId']}")
    else:
        st.error("Error: Unable to write data onto the Blockchain.")

