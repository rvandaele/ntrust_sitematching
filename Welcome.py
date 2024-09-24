import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="National Trust Matching Tool",
    page_icon="",
)



st.write("# Welcome to the National Trust Site Matching Tool! 👋")

st.sidebar.success("Select a site matching tool above")

st.markdown(
    """
    The National Trust Matching Tool is an open-source application built specifically for matching National Trust sites according to their specificities and climate parameters.
    
    
    **👈 Select a demo from the sidebar** to see some examples
    of what our tool can do!
    ### Want to learn more?
    - Check out the [LCAT](https://lcat.uk/) tool for more information about adaptation to climate change
    - Delve into the [UKCP](https://www.metoffice.gov.uk/research/approach/collaboration/ukcp) projection data used to build this tool
    - Ask us a question [by e-mail](r.vandaele@exeter.ac.uk)
"""
)

st.image(Image.open('data/national-trust-logo.png'), width=500)
