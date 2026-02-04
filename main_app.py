import streamlit as st
from mrv_engine import get_satellite_data, run_ai_audit
import pandas as pd

# --- WEB PAGE CONFIG ---
st.set_page_config(page_title="PeerCarbon MRV", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("Configuration")
lat = st.sidebar.number_input("Latitude", value=-1.28)
lon = st.sidebar.number_input("Longitude", value=36.82)
date_range = st.sidebar.date_input("Select Audit Period", [])

# --- MAIN INTERFACE ---
st.title("☀️ PeerCarbon Digital MRV")
st.info("Satellite-Verified Carbon Credit Issuance")

# Start Audit Button
if st.sidebar.button("Run Audit"):
    if len(date_range) == 2:
        start_str = date_range[0].strftime('%Y%m%d')
        end_str = date_range[1].strftime('%Y%m%d')
        
        with st.spinner("Fetching Satellite Truth Data..."):
            df = get_satellite_data(lat, lon, start_str, end_str)
            
            if df is not None:
                # 1. Simulate user meter data
                # Most days are honest (18% efficiency)
                df['Meter_Reading'] = df['Sunlight'] * 0.18 
                # Create a fake "Fraud" spike on the last day to test the AI
                df.iloc[-1, df.columns.get_loc('Meter_Reading')] *= 5 
                
                # 2. Run the Audit Logic from mrv_engine.py
                df = run_ai_audit(df)
                
                # 3. DISPLAY METRICS (The fix is here!)
                c1, c2 = st.columns(2)
                
                # Metric 1: Carbon Credits
                verified_co2 = df[df['Status']=='✅ Verified']['Meter_Reading'].sum() * 0.45
                c1.metric("Verified Credits", f"{verified_co2:.2f} kg CO2")
                
                # Metric 2: Anomalies (Fixed the TypeError here)
                anomaly_count = len(df[df['Status']=='🚩 Suspicious'])
                c2.metric("Flagged Anomalies", anomaly_count)
                
                # 4. VISUALIZATIONS
                st.divider()
                st.subheader("Audit Results: Physics vs. Reported Data")
                # This shows the AI in action: Verified points vs Suspicious points
                st.scatter_chart(df, x="Sunlight", y="Meter_Reading", color="Status")
                
                st.subheader("Detailed Audit Log")
                st.dataframe(df[['Sunlight', 'Expected_Power', 'Meter_Reading', 'Status']], use_container_width=True)
                
                st.success("✅ Prototype Audit Completed Successfully.")
            else:
                st.error("NASA API Error: Could not fetch data for these dates/location.")
    else:
        st.warning("Please select a Start and End date in the sidebar.")
else:
    # This shows before the user clicks the button
    st.write("### 👈 Set your parameters and click 'Run Audit' in the sidebar.")
    st.image("https://img.icons8.com/clouds/200/null/satellite.png")