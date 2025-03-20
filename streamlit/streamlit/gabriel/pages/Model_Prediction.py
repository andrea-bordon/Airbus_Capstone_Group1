import streamlit as st
import pandas as pd
import numpy as np
import re
import random
import pickle
from fpdf import FPDF
from pycaret.classification import load_model  

# Set up the page configuration
st.set_page_config(page_title="Fuel Leak Model Prediction", layout="wide")

st.title("Fuel Leak Detection Model")

# Upload dataset
st.header("Upload Aircraft Dataset")
uploaded_file = st.file_uploader("Upload the MSN dataset (CSV format)", type=["csv"])

# Expected columns for schema validation
expected_columns = [
    "FUEL_USED_2", "FUEL_USED_3", "FUEL_USED_4", "FW_GEO_ALTITUDE", "VALUE_FOB",
    "VALUE_FUEL_QTY_CT", "VALUE_FUEL_QTY_FT1", "VALUE_FUEL_QTY_FT2", "VALUE_FUEL_QTY_FT3",
    "VALUE_FUEL_QTY_FT4", "VALUE_FUEL_QTY_LXT", "VALUE_FUEL_QTY_RXT", "FLIGHT_PHASE_COUNT",
    "FUEL_USED_1", "Flight", "MSN", "UTC_TIME"
]

msn_number = "##"  # Default MSN placeholder
leaks_detected = []  # Initialize variable

if uploaded_file:
    df = pd.read_csv(uploaded_file, delimiter =";")  # Load in smaller parts
    #df = pd.concat(df)  # Combine chunks after processing

    missing_columns = [col for col in expected_columns if col not in df.columns]
    
    # Extract MSN number from file name
    match = re.search(r"msn_(\d{2})", uploaded_file.name)
    if match:
        msn_number = match.group(1)
    else:
        st.warning("MSN code could not be extracted, set to default ##")
    
    if not missing_columns:
        st.success("Schema Verified")
    else:
        st.error(f"Incorrect Schema for Model. Verify features == {missing_columns}")

    # Preprocessing logic
    df['NEW_FLIGHT'] = df.groupby('Flight')['FLIGHT_PHASE_COUNT'].diff().lt(0)
    df['FLIGHT_INSTANCE'] = df.groupby('Flight')['NEW_FLIGHT'].cumsum()
    df['FLIGHT_ID'] = df['Flight'].astype(str) + "_" + df['FLIGHT_INSTANCE'].astype(str)
    df['START_FOB'] = df.groupby('FLIGHT_ID')['VALUE_FOB'].transform('first')
    df = df[df["FLIGHT_PHASE_COUNT"] == 8.0]
    df = df.sort_index()
    df['TOTAL_FUEL_USED'] = df['FUEL_USED_1'] + df['FUEL_USED_2'] + df['FUEL_USED_3'] + df['FUEL_USED_4']
    df['EXPECTED_FOB'] = df['START_FOB'] - df['TOTAL_FUEL_USED']
    df["FOB_DIFFERENCE"] = (df['EXPECTED_FOB'] - df['VALUE_FOB']).abs()
    df['FOB_CHANGE'] = df['VALUE_FOB'].diff().fillna(0)
    df['EXPECTED_FOB_CHANGE'] = -df['TOTAL_FUEL_USED'].diff().fillna(0)
    df['FUEL_LEAK_RATE'] = df['EXPECTED_FOB_CHANGE'] - df['FOB_CHANGE']
    df['TOTAL_FUEL_LW'] = df['VALUE_FUEL_QTY_LXT'] + df['VALUE_FUEL_QTY_FT1'] + df['VALUE_FUEL_QTY_FT2']
    df['TOTAL_FUEL_RW'] = df['VALUE_FUEL_QTY_RXT'] + df['VALUE_FUEL_QTY_FT3'] + df['VALUE_FUEL_QTY_FT4']
    df['LW_RW_DIFF'] = (df['TOTAL_FUEL_LW'] - df['TOTAL_FUEL_RW']).abs()
    df['FUEL_IN_TANKS'] = df['VALUE_FUEL_QTY_CT'] + df['VALUE_FUEL_QTY_FT1'] + df['VALUE_FUEL_QTY_FT2'] + df['VALUE_FUEL_QTY_FT3'] + df['VALUE_FUEL_QTY_FT4'] + df['VALUE_FUEL_QTY_LXT'] + df['VALUE_FUEL_QTY_RXT']
    df['CALC_VALUE_FOB_DIFF'] = df['FUEL_IN_TANKS'] - df['VALUE_FOB']
    df['START_FOB_VS_FOB_FUELUSED'] = df['START_FOB'] - (df['FUEL_IN_TANKS'] + df['TOTAL_FUEL_USED'])
    df['ALTITUDE_DIFF'] = df['FW_GEO_ALTITUDE'].diff().fillna(0)
    df['UTC_TIME'] = pd.to_datetime(df['UTC_TIME'])


    # Save the original Flight column    
    df_sorted = df.sort_values(by=['FLIGHT_ID', 'UTC_TIME']).reset_index(drop=True)
    flight_reference = df_sorted[['Flight']].reset_index(drop=True)  # Preserve flight reference

  
    # User selection for model execution
    st.header("Select Model Execution Option")
    execution_option = st.radio("Choose an execution method:", [
        f"Run on Entire Dataset (MSN {msn_number})",
        "Run on a Random Flight",
        "Select a Specific Flight"
    ])


    
    flight_code = None
    if execution_option == "Select a Specific Flight":
        flight_code = st.selectbox("Select Flight:", df_sorted["Flight"].unique())
        st.write(f"Running model for Flight: {flight_code}")
        df_sorted = df_sorted[df_sorted["Flight"] == flight_code]
        flight_reference = df_sorted[['Flight']].reset_index(drop=True)  # Preserve correct flight reference

    elif execution_option == "Run on a Random Flight":
        flight_code = random.choice(df_sorted["Flight"].unique())
        st.write(f"Randomly selected Flight: {flight_code}")
        df_sorted = df_sorted[df_sorted["Flight"] == flight_code]
        flight_reference = df_sorted[['Flight']].reset_index(drop=True)  # Preserve correct flight reference

    
    # Drop Flight-related columns after selection
    df_sorted = df_sorted.drop(columns=['FLIGHT_PHASE_COUNT', 'Flight', 'FLIGHT_INSTANCE'])
    df_sorted = df_sorted.select_dtypes(include=[np.number])

    # Load the PyCaret model
    with st.spinner("Loading model..."):
        model = load_model("model_f2")  # Make sure path is correct!

    


    if st.button("Detect for Leaks"):
        
        # Run model prediction
        predictions = model.predict(df_sorted)
        result_df = pd.DataFrame(predictions, columns=["Leak_Detected"])
        result_df = pd.concat([flight_reference, result_df], axis=1)
        leaks_detected = result_df.loc[result_df["Leak_Detected"] == 1, "Flight"].unique().tolist()
        
        if leaks_detected:
            st.warning(f"Possible Detected Leaks in Flights == {leaks_detected}")
        else:
            st.success("No Leaks Detected")



    
    # Generate report option
    st.header("Generate Report")
    if st.button("Generate PDF Report"):
        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, "Fuel Leak Detection Report", ln=True, align="C")
                self.ln(10)

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Aircraft MSN: {msn_number}", ln=True, align="L")
        if flight_code:
            pdf.cell(200, 10, f"Flight Number: {flight_code}", ln=True, align="L")
        pdf.cell(200, 10, f"Leak Detection Result: {'Leak Detected' if leaks_detected else 'No Leak Detected'}", ln=True, align="L")
        report_filename = "fuel_leak_report.pdf"
        pdf.output(report_filename)
        st.success("Report Generated Successfully")
        with open(report_filename, "rb") as file:
            st.download_button("Download Report", file, file_name=report_filename)
