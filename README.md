Flood Guardian AI

AI-Based Flood Risk Monitoring and Early Warning Prototype

Flood Guardian AI is a web-based project designed to demonstrate flood risk assessment using rainfall, water level, and drainage conditions. It also provides weather information and flood safety recommendations.

Features

- Flood Risk Assessment: Estimates risk as LOW, MODERATE, or HIGH using environmental conditions.
- Weather Dashboard: Displays live weather information using the OpenWeather API.
- AI Model Demonstration: Uses a Random Forest classifier to demonstrate flood-risk classification.
- Rainfall Overview: Visualizes rainfall information.
- Flood Incident Reporting: Allows users to record flood incidents.
- Flood Safety Recommendations: Displays safety guidance based on assessed risk.
- Flood Risk Map: Displays selected demonstration locations.
- Mobile-Friendly Access: The Streamlit web application can be accessed through a browser.

Technology Stack

- Python
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- OpenWeather API
- HTML and CSS

Run Locally

1. Clone this repository.

2. Open the project folder in a terminal.

3. Install the dependencies:
   
   "pip install -r requirements.txt"

4. Configure your OpenWeather API key using Streamlit secrets.

5. Start the application:
   
   "streamlit run app.py"

Important Disclaimer

This project is a demonstration prototype. The AI model uses illustrative training data and is not validated for real-world flood prediction. Map markers do not represent verified flood zones. Do not rely on this application for emergency decisions.

Project Status

Prototype developed for learning and hackathon demonstration.

Author

Flood Guardian AI Project Team
