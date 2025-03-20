import streamlit as st
import os

# Set up the app layout and default page configuration
st.set_page_config(page_title="Airbus Fuel Leak Detection", layout="wide")

# Display the main page content with a centered title
st.markdown(
    """
    <div style="text-align: center;">
        <h1>Airbus Fuel Leak Detection</h1>
        <h2>Predictive Maintenance Using Machine Learning</h2>
        <h3>Capstone Project</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Project Overview
st.header("Project Overview")
st.write(
    "This project focuses on predicting fuel leaks in Airbus aircraft using historical sensor data. Fuel leaks are typically detected visually after landing, leading to unplanned maintenance and operational disruptions. The objective of this project is to develop a predictive model that enhances the early detection of fuel leaks, reducing aircraft downtime and maintenance costs."
)

st.header("Problem Statement")
st.write(
    "Current automated fuel leak detection systems are inaccurate due to fuel volume measurement errors in the tanks. Causes of fuel leaks include tank sealant degradation and structural damage. Early detection using data analytics can help airlines prevent unexpected aircraft-on-ground (AOG) events and improve fleet reliability."
)

st.header("Objectives")
st.write(
    "- Develop a predictive model to detect fuel leaks before visual inspections."
    "- Enhance maintenance planning and reduce unplanned aircraft downtime."
)

# Navigation links for different pages
st.sidebar.title("Navigation")
st.sidebar.page_link("Main.py", label="Main Page")
st.sidebar.page_link("pages/Model_Prediction.py", label="Model Prediction")
