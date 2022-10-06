from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

import urllib.request
import json


class ClientDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Job Description', validators=[DataRequired()])
    company_profile = StringField('Company Profile', validators=[DataRequired()])
    benefits = StringField('Benefits', validators=[DataRequired()])
    has_company_logo = StringField('Has Company Logo', validators=[DataRequired()])
    has_questions = StringField('Has Questions', validators=[DataRequired()])
    requirements = StringField('Requirements', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    function = StringField('Function', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(title, description, company_profile, benefits,
                   has_company_logo, has_questions, requirements, industry, function):
    body = {"title": title, "description": description,
            "company_profile": company_profile, "benefits": benefits, "has_company_logo": has_company_logo,
            "has_questions": has_questions, "requirements": requirements,"industry": industry, "function": function}

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
        data['title'] = request.form.get('title')
        data['location'] = request.form.get('location')
        data['department'] = request.form.get('description')
        data['company_profile'] = request.form.get('company_profile')
        data['description'] = request.form.get('description')
        data['requirements'] = request.form.get('requirements')
        data['benefits'] = request.form.get('benefits')
        data['has_company_logo'] = request.form.get('has_company_logo')
        data['has_questions'] = request.form.get('has_questions')
        data['industry'] = request.form.get('industry')
        data['function'] = request.form.get('function')

        try:
            response = str(get_prediction(data['title'], data['description'],
                data['company_profile'], data['benefits'], data['has_company_logo'],
                data['has_questions'], data['has_questions'], data['industry'],
                data['function']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        # return redirect(url_for('predicted', response=response))
        return render_template('predicted.html', response=response)
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
