from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

app.config['secret_strip_key'] = "sk_test_C6cVBQSJPAgIdcqACcSopUJs"

@app.errorhandler(404)
def not_found(error):
    return error

from app.controllers import app as app