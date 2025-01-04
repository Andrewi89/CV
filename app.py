import streamlit as st
from datetime import datetime

# Get the current year
current_year = datetime.now().year

# Define a function

# Streamlit app
st.title("Title")
st.write("Subtitle")

# input
query = st.text_input("Enter your :")

#Footer
footer_col1, footer_col2, footer_col3 = st.columns([1,6,1])
with footer_col2:
    st.markdown("""
    <hr style="height:1px;border:none;color:#333;background-color:#333;" />
    <p style="text-align: center; color: grey;">
        &copy; {year} Andrew Ireland. All Rights Reserved.
    </p>
    """.format(year=current_year), unsafe_allow_html=True)
  
st.markdown("""
<small style="color: grey;">
       
***Disclaimer:**  
While I have aimed to make this calculator as accurate as possible, please note that the results are estimates. These estimates should be used to inform decisions but not as the sole basis for making significant financial commitments. The solar data utilized in this application is sourced from the Photovoltaic Geographical Information System (PVGIS).*
</small>
""", unsafe_allow_html=True)`