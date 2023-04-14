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
st.header("Verify Harvest Details:")
id = st.text_input("ID", "24")
orgId = st.text_input("Org ID", "203")
itemCategoryId = st.text_input("Item Category ID", "2")
name = st.text_input("Name", "ช่อดอก (Flowers)")
umId = st.text_input("Unit of Measure ID", "16")
description = st.text_input("Description", "ช่อดอก Flowers")
isActive = st.checkbox("Is Active", value=True)
createdBy = st.text_input("Created By", "31899")
createdAt = st.text_input("Created At", "1642153891233")
updatedBy = st.text_input("Updated By", "31899")
updatedAt = st.text_input("Updated At", "1658828564872")
gtin = st.text_input("GTIN", "")
refCode = st.text_input("Ref Code", value=None)
unitPrice = st.text_input("Unit Price", value=0)
itemCategory = st.text_input("Item Category", value="Product")
itemUM = st.text_input("Item Unit of Measure", value="kilogram")
itemUMAbbreviation = st.text_input("Item Unit of Measure Abbreviation", value="kg")

# Define the submit button
if st.button("Submit"):
    # Define the request payload
    payload = {
        "id": id,
        "orgId": orgId,
        "itemCategoryId": itemCategoryId,
        "name": name,
        "umId": umId,
        "Description": description,
        "isActive": isActive,
        "createdBy": createdBy,
        "createdAt": createdAt,
        "updatedBy": updatedBy,
        "updatedAt": updatedAt,
        "Gtin": gtin,
        "refCode": refCode,
        "unitPrice": unitPrice,
        "itemCategory": itemCategory,
        "itemUM": itemUM,
        "itemUMAbbreviation": itemUMAbbreviation
    }

    # Call the API and handle the response
    with st.spinner("Loading... Please Wait"):
        response = requests.post("https://ecu-api.avalue.co.th/api/cnb/harvest", json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Success! isCreate: {result['isCreate']}, hashId: {result['hashId']}")
    else:
        st.error("Error: Unable to write data onto the Blockchain.")
