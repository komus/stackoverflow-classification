from flask import Flask
from flask_restful import Resource, Api
import numpy as np
from app.predict import *

app = Flask(__name__)
api = Api(app)


api.add_resource(SaySomething, '/')
api.add_resource(PredictUsingKmeans, '/predict')


if __name__ == '__main__':
    app.run(debug=True, port=5001)