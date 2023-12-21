import streamlit as st

colors = ['red', 'green', 'yellow', 'blue']

color_input = st.multiselect('Select options', colors, colors[:])
