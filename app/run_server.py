# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os

dill._dill._reverse_typemap['ClassType'] = type
# import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    with open(model_path, 'rb') as f:
        m = dill.load(f)
    return m


modelpath = "app/models/xgb_pipeline.dill"
model = load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        title, description, company_profile, benefits, \
        has_company_logo, has_questions, requirements, industry, function = "", "", "", "", "", "", "", "", ""
        request_json = flask.request.get_json()

        if request_json["title"]:
            title = request_json['title']

        if request_json["description"]:
            description = request_json['description']

        if request_json["company_profile"]:
            company_profile = request_json['company_profile']

        if request_json["benefits"]:
            benefits = request_json['benefits']

        if request_json["has_company_logo"]:
            has_company_logo = int(request_json['has_company_logo'])

        if request_json["has_questions"]:
            has_questions = int(request_json['has_questions'])

        if request_json["requirements"]:
            requirements = request_json['requirements']

        if request_json["industry"]:
            industry = request_json['industry']

        if request_json["function"]:
            function = request_json['function']

        logger.info(f'{dt} Data: title={title}, description={description}, '
                    f'company_profile={company_profile}, benefits={benefits}, has_company_logo={has_company_logo}, '
                    f'has_questions={has_questions}, requirements={requirements}, industry={industry}, '
                    f'function={function}')
        try:
            preds = model.predict_proba(pd.DataFrame({"title": [title],
                "description": [description], "company_profile": [company_profile],
                "benefits": [benefits], "has_company_logo": [has_company_logo],
                "has_questions": [has_questions], "requirements": [requirements],
                "industry": [industry], "function": [function]}))

        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = str(preds[:, 1][0])

        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
