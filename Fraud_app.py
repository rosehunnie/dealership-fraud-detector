# fraud_app.py
# Fraud_app.py

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# Page config
st.set_page_config(page_title="Dealership Fraud Detector", layout="wide")
st.title("🕵️‍♂️ AI-Powered Dealership Fraud & Anomaly Detector")

# File upload
uploaded_file = st.file_uploader("📤 Upload a spreadsheet (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Preview data
        st.subheader("📊 Uploaded Data Preview")
        st.write(df.head())

        # Show column types
        st.subheader("🧪 Original Column Data Types")
        st.write(df.dtypes)

        # Convert to numeric where possible
        df_numeric = df.apply(pd.to_numeric, errors='coerce')

        # Drop completely empty columns
        df_numeric = df_numeric.dropna(axis=1, how='all')

        # Select numeric columns
        numeric_cols = df_numeric.select_dtypes(include=['float64', 'int64']).columns
        st.subheader("🔍 Numeric Columns Detected")
        st.write(list(numeric_cols))

        if len(numeric_cols) < 1:
            st.warning("⚠️ No numeric columns detected for fraud analysis. Please check your data formatting.")
        else:
            # Run Isolation Forest model
            st.subheader("⚙️ Running Anomaly Detection...")
            iso = IsolationForest(contamination=0.02, random_state=42)

            # 🔧 FIX: convert column names to strings
            df_numeric.columns = df_numeric.columns.astype(str)
            numeric_cols = [str(col) for col in numeric_cols]

            # Fit model
            df['Anomaly_Score'] = iso.fit_predict(df_numeric[numeric_cols])

            # Get anomalies
            anomalies = df[df['Anomaly_Score'] == -1]

            # Display results
            st.error(f"⚠️ {len(anomalies)} potential anomalies detected.")
            st.dataframe(anomalies)

            # Download results
            st.download_button(
                label="📥 Download Anomalies as CSV",
                data=anomalies.to_csv(index=False),
                file_name="fraud_anomalies.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
