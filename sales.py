import streamlit as st
import pandas as pd
import requests
import time

# Load data from CSV file
data = pd.read_csv("Cantrak-on-Blockchain\cantrak_data_sales.csv", encoding="TIS-620")

# Set page title and add image
st.set_page_config(page_title="Cantrak on Polygon Blockchain", page_icon=":herb:")

# Define the input form for the user to select a Transaction ID
# First part - Cultivation Data
st.header("Sales Data")
selected_id = st.selectbox("Transaction ID", data["Transaction ID"])

# Get the row corresponding to the selected Transaction ID
selected_row = data.loc[data["Transaction ID"] == selected_id].iloc[0]

transaction_id = st.text_input("Transaction ID", selected_row["Transaction ID"])
seller_license_number = st.text_input("Seller License Number", selected_row["Seller License Number"])
buyer_license_number = st.text_input("Buyer License Number", selected_row["Buyer License Number"])
transaction_date = st.text_input("Transaction Date", selected_row["Transaction Date"])
product_category = st.text_input("Product Category", selected_row["Product Category"])
product_name = st.text_input("Product Name", selected_row["Product Name"])
product_quantity = st.text_input("Quantity", selected_row["Quantity"])
uom = st.text_input("UoM", selected_row["UoM"])
price = st.text_input("Price", selected_row["Price"])

if st.button("Submit"):
    payload = {
        "Id": transaction_id,
        "seller_license_number": seller_license_number,
        "buyer_license_number": buyer_license_number,
        "transaction_date": transaction_date,
        "product_category": product_category,
        "product_name": product_name,
        "product_quantity": product_quantity,
        "um": uom,
        "price": price
    }

    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        start_time = time.time() # start the timer
        response = requests.post("https://ecu-api.avalue.co.th/api/cnb/sales", json=payload)
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