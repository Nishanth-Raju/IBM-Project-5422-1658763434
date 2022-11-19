import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
#from joblib import load
app = Flask(__name__)
model = pickle.load(open('decision_model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[int(x) for x in request.form.values()]]
    print(x_test)
    #sc = load('scalar.save')
    prediction = model.predict(x_test)
    print(prediction)
    output = prediction[0]
    if (output <= 9):
        pred = "Worst performance with mileage " + \
            str(prediction[0]) + ". gotta have some spare change for fuel"
    if (output > 9 and output <= 17.5):
        pred = "Low performance with mileage " + \
            str(prediction[0]) + ". keep the distance a little small."
    if (output > 17.5 and output <= 29):
        pred = "Medium performance with mileage " + \
            str(prediction[0]) + ". a street or two."
    if (output > 29 and output <= 46):
        pred = "High performance with mileage " + \
            str(prediction[0]) + ". normal rides will get the job done"
    if (output > 46):
        pred = "Very high performance with mileage " + \
            str(prediction[0])+". world tour I suppose."

    return render_template('index.html', prediction_text='{}'.format(pred))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
