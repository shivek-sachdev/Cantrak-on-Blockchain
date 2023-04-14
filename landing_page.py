import streamlit as st
import random

# Define the emojis and labels for each box
BOXES = {
    "Grow": {"emoji": "🌱", "label": "Growing ID"},
    "Harvest": {"emoji": "🌾", "label": "Harvest ID"},
    "Production": {"emoji": "🏭", "label": "Production ID", "additional_label": "Process Name"},
    "Sales": {"emoji": "💰", "label": "Sales ID", "additional_label": "Sales Amount"},
}

# Define a function to generate a random emoji for each box
def get_random_emoji():
    return random.choice(["🍎", "🍇", "🍅", "🍓", "🥕", "🍆", "🥦", "🌽", "🥒"])

# Define the Streamlit app
def app():
    st.set_page_config(page_title="Select an option")

    # Render the boxes at the top of the page
    st.title("Select an option")
    selected_box = st.radio("", list(BOXES.keys()))

    # Render the form based on the selected box
    st.subheader(f"{BOXES[selected_box]['emoji']} {selected_box}")
    data_input = st.text_input(BOXES[selected_box]["label"])

    # Render additional input field and label for Production and Sales boxes
    if selected_box in ["Production", "Sales"]:
        additional_label = BOXES[selected_box]["additional_label"]
        additional_input = st.text_input(additional_label)

if __name__ == "__main__":
    app()
