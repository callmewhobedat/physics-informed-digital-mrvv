# ☀️ PeerCarbon: Digital MRV Dashboard
**Physics-Informed Carbon Credit Verification using Satellite Intelligence**

PeerCarbon is a Digital Monitoring, Reporting, and Verification (dMRV) prototype. It solves the "Trust Problem" in carbon markets by cross-referencing user-reported solar data with real-time satellite weather data from the NASA POWER API.



## 🚀 Key Features
* **Satellite Ground Truth:** Automatically fetches solar irradiance and temperature data based on GPS coordinates.
* **Physics-Informed Audit:** Uses a PV-performance model (Digital Twin) to calculate expected energy yield.
* **AI Fraud Detection:** Implements an `Isolation Forest` anomaly detection model to flag suspicious claims or hardware faults.
* **Automated Issuance:** Calculates verified CO2 avoided and potential carbon credit payouts.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/)
* **Data Science:** Pandas, NumPy, Scikit-Learn
* **API:** NASA POWER (Meteorological & Solar Data)
* **Logic:** Physics-based de-rating models + Unsupervised Machine Learning

## 📦 Installation & Setup
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/peercarbon-mrv.git](https://github.com/YOUR_USERNAME/peercarbon-mrv.git)
   cd peercarbon-mrv