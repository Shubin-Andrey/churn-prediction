
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired

import urllib.request
import json

class ClientDataForm(FlaskForm):

    CreditScore = StringField('CreditScore', validators=[DataRequired()])
    Age = StringField('Age', validators=[DataRequired()])
    Balance = StringField('Balance', validators=[DataRequired()])
    NumOfProducts = StringField('NumOfProducts', validators=[DataRequired()])
    EstimatedSalary = StringField('EstimatedSalary', validators=[DataRequired()])
    Geography = SelectField('Geography', choices=['France', 'Spain', 'Germany'])
    Gender = SelectField('Gender', choices=['Female', 'Male'])
    Tenure = SelectField('Tenure', choices=[ '2', ' 1',  '8',  '7',  '4',  '6',  '3', '10',  '5',  '9',  '0'])
    HasCrCard = SelectField('HasCrCard', choices=['1', '0'])
    IsActiveMember = SelectField('IsActiveMember', choices=['1', '0'])

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(body):
    for keys_ in body:
        body[keys_] = [body[keys_]]
    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)

@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['Geography'] = request.form.get('Geography')
        data['Gender'] = request.form.get('Gender')
        data['Tenure'] = request.form.get('Tenure')
        data['HasCrCard'] = request.form.get('HasCrCard')
        data['IsActiveMember'] = request.form.get('IsActiveMember')
        data['CreditScore'] = request.form.get('CreditScore')
        data['Age'] = request.form.get('Age')
        data['Balance'] = request.form.get('Balance')
        data['NumOfProducts'] = request.form.get('NumOfProducts')
        data['EstimatedSalary'] = request.form.get('EstimatedSalary')


        try:
            response = str(get_prediction(data))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)