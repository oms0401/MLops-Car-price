import streamlit as st
import requests
import os


API_URL = os.getenv("FASTAPI_URL", "https://mlops-car-price-1.onrender.com/")
API_KEY = os.getenv("API_KEY", "demo-key") 

# --- Page Setup ---
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)
st.title("🚗 Car Price Prediction")

# --- Authentication (in sidebar) ---
# Use session state to keep the user logged in.
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

with st.sidebar:
    st.header("Login")
    # Use the hardcoded credentials from your auth router
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", value="admin", type="password")

    if st.button("Login"):
        login_payload = {
            "username": username,
            "password": password
        }
        try:
            # The login endpoint path is /login
            response = requests.post("https://mlops-car-price-1.onrender.com/login", json=login_payload)
            if response.status_code == 200:
                # The token is in the 'access_token' field
                st.session_state.auth_token = response.json().get("access_token")
                st.success("Login Successful!")
            else:
                st.error(f"Login failed. Status: {response.status_code}")
                st.json(response.json())
                st.session_state.auth_token = None
        except requests.exceptions.RequestException as e:
            st.error(f"Connection to API failed: {e}")

    if st.session_state.auth_token:
        st.success("Logged in successfully.")
    else:
        st.info("Please log in to make predictions.")

# --- Prediction Interface ---
st.header("Enter Car Details to Predict Price")

if not st.session_state.auth_token:
    st.warning("You must be logged in to use the prediction feature.")
else:
    # Create a form for a cleaner UI
    with st.form("prediction_form"):
        # Use columns for a better layout, similar to the template
        col1, col2 = st.columns(2)

        with col1:
            # Updated with all 32 brands, sorted alphabetically
            company = st.selectbox(
                "Brand",
                sorted(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault', 'Mahindra',
                        'Tata', 'Chevrolet', 'Fiat', 'Datsun', 'Jeep', 'Mercedes-Benz', 'Mitsubishi',
                        'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus', 'Jaguar', 'Land', 'MG', 'Volvo',
                        'Daewoo', 'Kia', 'Force', 'Ambassador', 'Ashok', 'Isuzu', 'Opel', 'Peugeot'])
            )
            year = st.number_input("Manufacturing Year", min_value=1990, max_value=2024, value=2015, step=1)
            km_driven = st.number_input("Kilometers Driven", min_value=0, value=50000, step=1000)
            # Updated with the correct fuel types
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG"])
            seller_type = st.selectbox("Seller Type", ["Individual", "Dealer", "Trustmark Dealer"])
            transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

        with col2:
            # Updated to include "Test Drive Car"
            owner = st.selectbox("Owner", ["First", "Second", "Third", "Fourth & Above", "Test Drive Car"])
            mileage_mpg = st.number_input("Mileage (in MPG)", min_value=5.0, max_value=60.0, value=20.0, step=0.1, format="%.1f")
            engine_cc = st.number_input("Engine (in CC)", min_value=600, max_value=6000, value=1500, step=50)
            max_power_bhp = st.number_input("Max Power (in BHP)", min_value=30.0, max_value=600.0, value=90.0, step=1.0, format="%.1f")
            torque_nm = st.number_input("Torque (in Nm)", min_value=40.0, max_value=800.0, value=150.0, step=5.0, format="%.1f")
            seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5, step=1)

        # Predict button for the form
        calculator = st.form_submit_button(label="Calculate price")

    if calculator:
        # Construct the JSON payload from the form inputs
        input_data = {
            "company": company,
            "year": year,
            "owner": owner,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "km_driven": float(km_driven),
            "mileage_mpg": float(mileage_mpg),
            "engine_cc": float(engine_cc),
            "max_power_bhp": float(max_power_bhp),
            "torque_nm": float(torque_nm),
            "seats": float(seats)
        }

        headers = {
            "token": st.session_state.auth_token,  
            "api-key": API_KEY                     
        }

        try:
            with st.spinner("Calculating... Please wait."):
                result = requests.post("https://mlops-car-price-1.onrender.com/predict", json=input_data, headers=headers)

                if result.status_code == 200:
                    # The prediction is in the 'predicted_price' field
                    price = result.json().get("predicted_price")
                    st.success(f"### Predicted Price: ₹ {price}")
                elif result.status_code == 401:
                    st.error("Authentication Error. Your login may have expired. Please log in again.")
                else:
                    st.error(f"Prediction failed. Server returned status {result.status_code}.")
                    st.json(result.json()) # Show detailed error from the API

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the prediction API: {e}")

