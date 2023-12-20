import streamlit as st

query_params = st.experimental_get_query_params()
page = query_params.get("page", None)

if page == "next":
    print("ff")
    # Navigate to the next page
