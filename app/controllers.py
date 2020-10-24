import stripe

from app import app

from flask import request, jsonify, render_template

stripe.api_key = app.config['secret_strip_key']