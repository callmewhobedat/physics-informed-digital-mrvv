import requests
import pandas as pd
from sklearn.ensemble import IsolationForest  # Moved to top

def get_satellite_data(lat, lon, start, end):
    """Fetches real solar and temp data from NASA"""
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN,T2M&community=RE&longitude={lon}&latitude={lat}&start={start}&end={end}&format=JSON"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        sun = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        temp = data['properties']['parameter']['T2M']
        
        df = pd.DataFrame({'Sunlight': sun, 'Temp': temp})
        # Convert index to datetime for easier joining later
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"Error fetching NASA data: {e}")
        return None

def run_ai_audit(df, efficiency=0.20):
    """Physics + AI Anomaly Detection"""
    # 1. Physics Calculation (Digital Twin)
    # Formula: Sunlight * Efficiency * Temperature Derating Factor
    df['Expected_Power'] = df['Sunlight'] * efficiency * (1 - 0.004 * (df['Temp'] - 25))
    
    # 2. AI Anomaly Detection
    # We use Sunlight and Meter_Reading to find points that don't 'fit' the pattern
    X = df[['Sunlight', 'Meter_Reading']].values
    model = IsolationForest(contamination=0.1, random_state=42)
    df['Anomaly_Score'] = model.fit_predict(X)
    
    # 3. Decision Logic
    df['Status'] = "✅ Verified"
    
    # Flag if AI says it's an outlier (-1) OR if it significantly exceeds physics (1.2 multiplier)
    mask = (df['Anomaly_Score'] == -1) | (df['Meter_Reading'] > df['Expected_Power'] * 1.2)
    df.loc[mask, 'Status'] = "🚩 Suspicious"
    
    return df
