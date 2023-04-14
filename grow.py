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

