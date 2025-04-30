# fraud_app.py

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Dealership Fraud Detector", layout="wide")
st.title("🕵️‍♂️ AI-Powered Dealership Fraud & Anomaly Detector")

# Upload file
uploaded_file = st.file_uploader("📤 Upload a spreadsheet (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Preview data
        st.subheader("📊 Uploaded Data Preview")
        st.write(df.head())

        # Show original column data types
        st.subheader("🧪 Original Column Data Types")
        st.write(df.dtypes)

        # Try converting all columns to numeric if possible
        df_numeric = df.apply(pd.to_numeric, errors='coerce')

        # Drop empty columns
        df_numeric = df_numeric.dropna(axis=1, how='all')

        # Detect usable numeric columns
        numeric_cols = df_numeric.select_dtypes(include=['float64', 'int64']).columns
        st.subheader("🔍 Numeric Columns Detected")
        st.write(list(numeric_cols))

        if len(numeric_cols) < 1:
            st.warning("⚠️ No numeric columns found for fraud analysis. Please check the format of your data.")
        else:
            # Run Isolation Forest
            st.subheader("⚙️ Running Anomaly Detection...")
            iso = IsolationForest(contamination=0.02, random_state=42)
            df['Anomaly_Score'] = iso.fit_predict(df_numeric[numeric_cols])

            # Extract anomaly rows
            anomalies = df[df['Anomaly_Score'] == -1]

            # Show results
            st.error(f"⚠️ {len(anomalies)} potential anomalies detected.")
            st.dataframe(anomalies)

            # Allow CSV download of anomalies
            st.download_button(
                label="📥 Download Anomalies as CSV",
                data=anomalies.to_csv(index=False),
                file_name="fraud_anomalies.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
