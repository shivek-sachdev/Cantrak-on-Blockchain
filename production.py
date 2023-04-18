import streamlit as st
import pandas as pd
import requests
import time

# Load data from CSV file
data = pd.read_csv("Cantrak-on-Blockchain\cantrak_data_production.csv", encoding="TIS-620")

# Set page title and add image
st.set_page_config(page_title="Cantrak on Polygon Blockchain", page_icon=":herb:")

# Define the input form for the user to select a Transaction ID
# First part - Cultivation Data
st.header("Production Data")
selected_id = st.selectbox("Transaction ID", data["Transaction ID"])

# Get the row corresponding to the selected Transaction ID
selected_row = data.loc[data["Transaction ID"] == selected_id].iloc[0]

# Display the rest of the data for the selected Transaction ID
transaction_id = st.text_input("Transaction ID", selected_row["Transaction ID"])
production_lot_number = st.text_input("Production Lot Number", selected_row["Production Lot Number"])
process_name = st.text_input("Process Name", selected_row["Process Name"])
item_category = st.text_input("Item Category", selected_row["Item Category"])
item_name = st.text_input("Item Name", selected_row["Item Name"])
description = st.text_input("Description", selected_row["Description"])
quantity_prodcued = st.text_input("Quantity Produced", selected_row["Quantity Produced"])
uom = st.text_input("UoM", selected_row["UoM"])
expiry_date = st.text_input("Expiry Date", selected_row["Expiry Date"])
ref_plant_lot_name = st.text_input("Ref. Plant Lot Name", selected_row["Ref. Plant Lot Name"])
ref_plant_lot_number = st.text_input("Ref. Plant Lot Number", selected_row["Ref. Plant Lot Number"])
extraction_license_number = st.text_input("Extraction License Number", selected_row["Extraction License Number"])
created_date = st.text_input("Created Date", selected_row["Created Date"])
created_by = st.text_input("Created By", selected_row["Created By"])
status = st.text_input("Status", selected_row["Status"])

# Define the submit button
if st.button("Submit"):
    # Define the request payload
    payload = {
        "id": transaction_id,
        "productionLotNo": production_lot_number,
        "processName": process_name,
        "itemCategoryName": item_category,
        "itemName": item_name,
        "description": description,
        "quantity": quantity_prodcued,
        "um": uom,
        "expirydate": expiry_date,
        "plantlotname": ref_plant_lot_name,
        "plantlotnumber": ref_plant_lot_number,
        "licensenumber": extraction_license_number,
        "createddate": created_date,
        "createdby": created_by,
        "isActive": status
    }

    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        start_time = time.time() # start the timer
        response = requests.post("https://ecu-api.avalue.co.th/api/cnb/production", json=payload)
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
        with st.spinner("Loading... Please Wait"):
            url = f"https://ecu-api.avalue.co.th/api/cnb/production/{transaction_id}"
            response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
            #st.success(f"Success! hashId: {result['hashId']}")
            st.success(f"Validate your transaction here: {result['explorerURL']}")
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