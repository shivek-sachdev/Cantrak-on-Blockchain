import streamlit as st

# Define your pages/views as Python functions
def home():
    st.title("Welcome to my app!")
    st.write("This is the home page.")

def page1():
    st.title("Page 1")
    st.write("This is page 1.")

def page2():
    st.title("Page 2")
    st.write("This is page 2.")

# Define a dictionary that maps page names to functions
PAGES = {
    "Home": home,
    "Page 1": page1,
    "Page 2": page2,
}

# Render the navigation menu and page content based on the selected menu item
def app():
    st.set_page_config(page_title="Multi-page app")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("", list(PAGES.keys()))

    page = PAGES[selection]
    page()

if __name__ == "__main__":
    app()
