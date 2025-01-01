import streamlit as st
import pickle
import pandas as pd

# Load the pre-trained preprocessing pipeline, model, and label encoder
pipeline = pickle.load(open('preprocessing_pipeline.pkl','rb'))
model = pickle.load(open('finalmodel.pkl', 'rb'))

def user_input_features():
    st.sidebar.header('User Input Parameters')

    # Last contact date - Using text input (you can parse this into datetime)
    last_contact_date = st.sidebar.date_input("Last Contact Date")

    # Age - Using a slider
    age = st.sidebar.slider("Age", 18, 100, 30)

    # Job - Dropdown selection
    job = st.sidebar.selectbox("Job", ["admin.", "blue-collar", "entrepreneur", "housemaid", 
                                      "management", "retired", "self-employed", "services", 
                                      "student", "technician", "unemployed", "unknown"])

    # Marital - Dropdown selection
    marital = st.sidebar.selectbox("Marital Status", ["married", "divorced", "single"])

    # Education - Dropdown selection
    education = st.sidebar.selectbox("Education", ["primary", "secondary", "tertiary", "unknown"])

    # Default - Checkbox (whether the person has credit in default)
    default = st.sidebar.selectbox("Has Default?", ["yes", "no"])

    # Balance - Numeric input
    balance = st.sidebar.number_input("Balance", min_value=-1000, max_value=100000, value=0)

    # Housing - Checkbox (whether the person has a housing loan)
    housing = st.sidebar.selectbox("Has Housing Loan?", ["yes", "no"])

    # Loan - Checkbox (whether the person has a personal loan)
    loan = st.sidebar.selectbox("Has Personal Loan?", ["yes", "no"])

    # Contact - Dropdown selection
    contact = st.sidebar.selectbox("Contact Communication Type", ["cellular", "telephone", "unknown"])

    # Duration - Slider (duration of the last contact in seconds)
    duration = st.sidebar.slider("Duration of Last Contact (seconds)", 0, 5000, 100)

    # Campaign - Slider (number of contacts performed during the campaign)
    campaign = st.sidebar.slider("Number of Contacts in Campaign", 1, 100, 1)

    # Pdays - Slider (number of days since the last contact)
    pdays = st.sidebar.slider("Days Since Last Contact", -1, 1000, -1)

    # Previous - Slider (number of contacts performed before this campaign)
    previous = st.sidebar.slider("Number of Previous Contacts", 0, 100, 0)

    # Poutcome - Dropdown selection
    poutcome = st.sidebar.selectbox("Outcome of Previous Marketing Campaign", ["failure", "nonexistent", "success"])

    # Target - Checkbox (whether the customer subscribed to a term deposit)
    target = st.sidebar.selectbox("Subscribed to Term Deposit?", ["yes", "no"])

    # Return input as a dictionary
    user_data = {
        'last_contact_date': last_contact_date,
        'age': age,
        'job': job,
        'marital': marital,
        'education': education,
        'default': default,
        'balance': balance,
        'housing': housing,
        'loan': loan,
        'contact': contact,
        'duration': duration,
        'campaign': campaign,
        'pdays': pdays,
        'previous': previous,
        'poutcome': poutcome,
        'target': target
    }
    return user_data

# Main function to run the app
def main():
    st.title("Customer Data Input for Prediction")

    # Get user input features
    user_data = user_input_features()

    # Convert the user input into a DataFrame for processing
    input_df = pd.DataFrame(user_data, index=[0])

    # Apply preprocessing pipeline
    processed_data = pipeline.transform(input_df)

    # Make prediction using the model
    prediction = model.predict(processed_data)

    # Display user input data
    st.write("### User Input Data", user_data)

    # Display prediction result
    if prediction[0] == 'yes':
        st.write("### Prediction: The customer is predicted to subscribe to a term deposit.")
    else:
        st.write("### Prediction: The customer is predicted not to subscribe to a term deposit.")

if __name__ == '__main__':
    main()
