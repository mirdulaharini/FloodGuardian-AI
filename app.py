import streamlit as st
from pathlib import Path

css = Path("style.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.set_page_config(
    page_title="Flood Guardian AI",
    page_icon="🌊",
    layout="wide"
)
import pandas as pd
import requests
from flood_model import predict_flood_risk

st.set_page_config(
    page_title="Flood Guardian AI",
    page_icon="🌧️",
    layout="wide"
)

st.title("Flood Guardian AI")
st.caption("Flood Risk Monitoring and Early Warning Prototype")

st.info(
    "Demonstration prototype using illustrative rules. "
    "It is not connected to live weather data or official alerts."
)

# Sidebar inputs
st.sidebar.header("Location Details")

location = st.sidebar.text_input(
    "Village or city",
    value="Thanjavur"
)

st.sidebar.header("Environmental Conditions")

rainfall = st.sidebar.number_input(
    "Rainfall in the last 24 hours (mm)",
    min_value=0.0,
    max_value=1000.0,
    value=20.0,
    step=5.0
)

water_level = st.sidebar.selectbox(
    "River or water level",
    ["Normal", "Rising", "High", "Overflowing"]
)

drainage = st.sidebar.selectbox(
    "Drainage condition",
    ["Clear", "Partially blocked", "Blocked"]
)

# Dashboard summary
st.subheader("Environmental Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rainfall", f"{rainfall:.0f} mm")

with col2:
    st.metric("Water Level", water_level)

with col3:
    st.metric("Drainage", drainage)

# Rainfall visualization
st.subheader("Rainfall Overview")

rain_data = pd.DataFrame({
    "Measurement": ["Current entered rainfall"],
    "Rainfall (mm)": [rainfall]
})

import plotly.express as px

fig = px.bar(
    rain_data,
    x="Measurement",
    y="Rainfall (mm)",
    title="Rainfall in the Last 24 Hours",
    color_discrete_sequence=["#45d6c5"]
)

fig.update_layout(
    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",
    font_color="#e5edf7",
    title_font_color="#45d6c5",
    xaxis=dict(
        title="Measurement",
        gridcolor="#29415c"
    ),
    yaxis=dict(
        title="Rainfall (mm)",
        gridcolor="#29415c"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

# Risk analysis
st.subheader("Flood Risk Assessment")

if st.button("Analyze Flood Risk", type="primary"):

    score = 0

    if rainfall >= 150:
        score += 3
    elif rainfall >= 70:
        score += 2
    elif rainfall >= 30:
        score += 1

    if water_level == "Rising":
        score += 1
    elif water_level == "High":
        score += 2
    elif water_level == "Overflowing":
        score += 3

    if drainage == "Partially blocked":
        score += 1
    elif drainage == "Blocked":
        score += 2

    if score >= 6:
        risk = "HIGH"
        advice = (
            "Avoid floodwater and low-lying areas. "
            "Follow official emergency instructions."
        )
    elif score >= 3:
        risk = "MODERATE"
        advice = (
            "Monitor official weather and flood updates. "
            "Prepare for possible flooding."
        )
    else:
        risk = "LOW"
        advice = (
            "Continue monitoring local conditions. "
            "A low prototype score does not guarantee safety."
        )
        # AI model prediction (demonstration only)
        water_level_scores = {
            "Normal": 0,
            "Rising": 1,
            "High": 2,
            "Overflowing": 3
        }

        drainage_scores = {
            "Clear": 0,
            "Partially blocked": 1,
            "Blocked": 2
        }

        ai_risk = predict_flood_risk(
            rainfall,
            water_level_scores[water_level],
            drainage_scores[drainage]
        )

        st.subheader("AI Flood Risk Prediction")
        st.write("Model prediction:", ai_risk)
        if ai_risk == "HIGH":
            st.error(
                "HIGH FLOOD RISK: Avoid floodwater and low-lying areas. "
                "Follow official emergency instructions."
            )
        elif ai_risk == "MODERATE":
            st.warning(
                "MODERATE FLOOD RISK: Monitor weather and water levels. "
                "Prepare for possible flooding."
            )
        else:
            st.success(
                "LOW ESTIMATED RISK: Continue monitoring local conditions. "
                "Low risk does not guarantee safety."
            )
        st.caption(
            "Demonstration model trained on illustrative data. "
            "Not suitable for real-world flood warnings."
        )

    st.write("Location:", location or "Not specified")
    st.metric("Illustrative Risk Score", f"{score}/8")

    if risk == "HIGH":
        st.error(f"Estimated Risk: {risk}")
    elif risk == "MODERATE":
        st.warning(f"Estimated Risk: {risk}")
    else:
        st.success(f"Estimated Risk: {risk}")

    st.write("### Recommended Safety Action")
    st.write(advice)
    st.session_state.alert_history.append({
            "Location": location,
            "Rainfall (mm)": rainfall,
            "Water Level": water_level,
            "Drainage": drainage,
            "Risk Level": risk
        })

    st.caption(
        "This score uses demonstration rules, not a trained "
        "AI model. It is not an official flood prediction."
    )
    # Flood Alert History
if "alert_history" not in st.session_state:
    st.session_state.alert_history = []

st.divider()
st.header("Flood Alert History")

if st.session_state.alert_history:
    history_df = pd.DataFrame(st.session_state.alert_history)
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No flood risk analyses have been recorded yet.")
# Flood Incident Reporting
st.divider()
st.header("Report a Flood Incident")
st.write("Submit a report about flooding in your area.")

if "flood_reports" not in st.session_state:
    st.session_state.flood_reports = []

with st.form("flood_report_form"):
    report_location = st.text_input(
        "Affected location",
        placeholder="Enter village, town, or area"
    )

    incident_type = st.selectbox(
        "Type of incident",
        [
            "Waterlogging",
            "River overflow",
            "Road flooding",
            "Drainage blockage",
            "Other"
        ]
    )

    severity = st.selectbox(
        "Reported severity",
        ["Low", "Moderate", "Severe"]
    )

    description = st.text_area(
        "Describe the situation",
        placeholder="Describe what you observed"
    )

    submitted = st.form_submit_button("Submit Flood Report")

    if submitted:
        if not report_location.strip():
            st.error("Please enter the affected location.")
        else:
            report = {
                "Location": report_location.strip(),
                "Incident": incident_type,
                "Severity": severity,
                "Description": description
            }

            st.session_state.flood_reports.append(report)
            st.success("Flood report submitted successfully.")

# Display submitted reports
if st.session_state.flood_reports:
    st.subheader("Submitted Flood Reports")

    for number, report in enumerate(
        st.session_state.flood_reports, start=1
    ):
        with st.expander(
            f"Report {number}: {report['Location']}"
        ):
            st.write("Incident:", report["Incident"])
            st.write("Severity:", report["Severity"])
            st.write(
                "Description:",
                report["Description"] or "No description provided"
            )
st.divider()
st.caption("Flood Guardian AI | Hackathon Prototype")
# Download flood reports
if st.session_state.flood_reports:
    st.divider()
    st.subheader("Export Flood Reports")

    reports_df = pd.DataFrame(
        st.session_state.flood_reports
    )

    csv_data = reports_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Reports as CSV",
        data=csv_data,
        file_name="flood_reports.csv",
        mime="text/csv"
    )
    # Live Weather from OpenWeather
st.divider()
st.header("Live Weather")

city = st.text_input("Enter city name", "Thanjavur")

if st.button("Get Live Weather"):
    api_key = st.secrets["OPENWEATHER_API_KEY"]

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            weather = response.json()

            st.success(f"Weather found for {weather['name']}")
            st.write("Temperature:", weather["main"]["temp"], "°C")
            st.write("Humidity:", weather["main"]["humidity"], "%")
            st.write("Conditions:", weather["weather"][0]["description"])

            rain = weather.get("rain", {})
            rainfall = rain.get("1h", rain.get("3h", None))
            st.write("Recent rainfall:", f"{rainfall} mm" if rainfall is not None else "Not available")

        elif response.status_code == 401:
            st.error("API key is not active or is invalid. Check your OpenWeather account.")
        elif response.status_code == 404:
            st.error("City not found. Check the spelling.")
        else:
            st.error(f"Weather service returned error {response.status_code}.")

    except requests.RequestException:
        st.error("Could not connect to the weather service. Check your internet connection.")

        # Flood Safety Recommendations
st.divider()
st.header("Flood Safety Recommendations")
# Rainfall Trend Dashboard
st.divider()
st.header("Rainfall Trend Dashboard")
st.write(
    "Record rainfall readings to observe changes over time. "
    "These are manually entered readings, not historical weather data."
)

if "rainfall_history" not in st.session_state:
    st.session_state.rainfall_history = []

rainfall_value = st.number_input(
    "Rainfall reading (mm)",
    min_value=0.0,
    max_value=1000.0,
    value=10.0,
    step=5.0,
    key="trend_rainfall_input"
)

if st.button("Record Rainfall Reading"):
    st.session_state.rainfall_history.append(
        {"Reading": len(st.session_state.rainfall_history) + 1,
         "Rainfall (mm)": rainfall_value}
    )

if st.session_state.rainfall_history:
    if st.button("Clear Rainfall Readings"):
     st.session_state.rainfall_history = []
    st.rerun()
    trend_df = pd.DataFrame(st.session_state.rainfall_history)
    st.line_chart(trend_df.set_index("Reading")["Rainfall (mm)"])
    if len(trend_df) >= 2:
        first_reading = trend_df["Rainfall (mm)"].iloc[0]
        latest_reading = trend_df["Rainfall (mm)"].iloc[-1]

        if latest_reading > first_reading:
            st.warning("Rainfall readings have increased.")
        elif latest_reading < first_reading:
            st.success("Rainfall readings have decreased.")
        else:
            st.info("Rainfall readings have stayed the same.")
    st.dataframe(trend_df, use_container_width=True)
    st.download_button(
        label="Download Rainfall Report",
        data=trend_df.to_csv(index=False),
        file_name="rainfall_report.csv",
        mime="text/csv"
    )
else:
    st.info("No readings recorded yet. Enter a reading and click Record.")

st.write("1. Avoid walking or driving through floodwater.")
st.write("2. Move away from rivers, canals, and overflowing drains.")
st.write("3. Keep your phone charged and emergency contacts ready.")
st.write("4. Follow official weather and disaster-management alerts.")
st.write("5. If flooding threatens your area, move to a safer place and follow official instructions.")

# Flood Risk Map
st.divider()
st.header("Flood Risk Map")
st.write("Select a location to display it on the map.")

map_location = st.selectbox(
    "Choose a demo location",
    ["Thanjavur", "Chennai", "Coimbatore", "Tiruchirappalli"]
)
locations = {
    "Thanjavur": {"lat": 10.7870, "lon": 79.1378},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "Tiruchirappalli": {"lat": 10.7905, "lon": 78.7047},
}

selected = locations[map_location]

st.write("Selected location:", map_location)
st.map(
    pd.DataFrame({
        "latitude": [selected["lat"]],
        "longitude": [selected["lon"]]
    })
)
st.caption(
    "Map markers show selected locations only. "
    "They do not represent verified flood zones or live flood conditions."
)