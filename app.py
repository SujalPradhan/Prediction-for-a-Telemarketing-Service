from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

app = Flask(__name__)

# Load the pre-trained preprocessing pipeline and model
pipeline = pickle.load(open('preprocessing_pipeline.pkl', 'rb'))
model = pickle.load(open('finalmodel.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Safely get form data using .get() method to avoid KeyError
        marital = request.form.get('marital')
        age = request.form.get('age', type=int)
        job = request.form.get('job')
        education = request.form.get('education')
        default = request.form.get('default')
        balance = request.form.get('balance', type=float)
        housing = request.form.get('housing')
        loan = request.form.get('loan')
        contact = request.form.get('contact')
        duration = request.form.get('duration', type=int)
        campaign = request.form.get('campaign', type=int)
        pdays = request.form.get('pdays', type=int)
        previous = request.form.get('previous', type=int)
        poutcome = request.form.get('poutcome')
        target = request.form.get('target')

        # Convert input data to a DataFrame
        user_data = {
            'marital': marital,
            'age': age,
            'job': job,
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

        input_df = pd.DataFrame(user_data, index=[0])

        # Apply preprocessing pipeline (make sure input_df is a DataFrame)
        processed_data = pipeline.transform(input_df)

        # Now pass the processed data to the model for prediction
        prediction = model.predict(processed_data)

        if prediction[0] == 'yes':
            prediction_text = "The customer is predicted to subscribe to a term deposit."
        else:
            prediction_text = "The customer is predicted not to subscribe to a term deposit."

        return render_template('index.html', prediction_text=prediction_text, user_data=user_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
