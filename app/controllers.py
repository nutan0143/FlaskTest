import stripe

from app import app

from flask import request, jsonify, render_template
from flask.views import MethodView

from datetime import datetime

stripe.api_key = app.config['secret_strip_key']

def bad_request_response(message):
	"""
		Bad Request Response
	"""
    context = {
        'errors': {"message": message},
        "status": False,
        "code": 400,
        "message": "Something went wrong!"
    }
    return jsonify(context)

class PremiumPaymentGateway(object):
	"""
		Premium payment gateway class
	"""
	def __init__(self,card_number,card_holder,expiry_month,expiry_year,amount,cvc=None):
		self.stripe = stripe
		self.card_number=card_number
		self.card_holder=card_holder
		self.expiry_month=expiry_month
		self.expiry_year=expiry_year
		self.amount=amount
		self.cvc=cvc

	def paymentIntent(self):
		try:
			payment_method_response = self.stripe.PaymentMethod.create(
				type="card",
				card={
				"number": self.card_number,
				"exp_month": self.expiry_month,
				"exp_year": self.expiry_year,
				"cvc": self.cvc,
				},
			)
			payment_intent = self.stripe.PaymentIntent.create(
				amount=self.amount,
				currency='gbp',
				payment_method_types=["card"],
				payment_method=payment_method_response["id"]
			)
			return {"status_action":True,"data":payment_intent}
		except stripe.error.InvalidRequestError as e:
			message = {
				"message": e.error.message,
				"status": e.http_status,
				"code": e.error.code,
				"parameter": e.error.param,
				"status_action":False
			}
			return message

class ExpensivePaymentGateway(object):
	"""
		Expensive payment gateway class
	"""
	def __init__(self,card_number,card_holder,expiry_month,expiry_year,amount,cvc=None):
		self.stripe = stripe
		self.card_number=card_number
		self.card_holder=card_holder
		self.expiry_month=expiry_month
		self.expiry_year=expiry_year
		self.amount=amount
		self.cvc=cvc

	def paymentIntent(self):
		try:
			payment_method_response = self.stripe.PaymentMethod.create(
				type="card",
				card={
				"number": self.card_number,
				"exp_month": self.expiry_month,
				"exp_year": self.expiry_year,
				"cvc": self.cvc,
				},
			)
			payment_intent = self.stripe.PaymentIntent.create(
				amount=self.amount,
				currency='gbp',
				payment_method_types=["card"],
				payment_method=payment_method_response["id"]
			)
			return {"status_action":True,"data":payment_intent}
		except stripe.error.InvalidRequestError as e:
			message = {
				"message": e.error.message,
				"status": e.http_status,
				"code": e.error.code,
				"parameter": e.error.param,
				"status_action":False
			}
			return message

class CheapPaymentGateway(object):
	"""
		Cheap payment gateway class
	"""
	def __init__(self,card_number,card_holder,expiry_month,expiry_year,amount,cvc=None):
		self.stripe = stripe
		self.card_number=card_number
		self.card_holder=card_holder
		self.expiry_month=expiry_month
		self.expiry_year=expiry_year
		self.amount=amount
		self.cvc=cvc

	def paymentIntent(self):
		try:
			payment_method_response = self.stripe.PaymentMethod.create(
				type="card",
				card={
				"number": self.card_number,
				"exp_month": self.expiry_month,
				"exp_year": self.expiry_year,
				"cvc": self.cvc,
				},
			)
			payment_intent = self.stripe.PaymentIntent.create(
				amount=self.amount,
				currency='gbp',
				payment_method_types=["card"],
				payment_method=payment_method_response["id"]
			)
			return {"status_action":True,"data":payment_intent}
		except stripe.error.InvalidRequestError as e:
			message = {
				"message": e.error.message,
				"status": e.http_status,
				"code": e.error.code,
				"parameter": e.error.param,
				"status_action":False
			}
			return message

class ProcessPayment(MethodView):
	"""
		Payment Intent using card
	"""
	def post(self):
		try:
			param = request.json
			current_date = datetime.now()
			if 'card_number' not in param or param['card_number'] == "" or param['card_number'] is None:
				return bad_request_response("Please enter card Number.")
			if 'card_holder' not in param or param['card_holder'] == "" or param['card_holder'] is None:
				return bad_request_response("Please enter card holder name.")
			if 'expiry_date' not in param or param['expiry_date'] == "" or param['expiry_date'] is None:
				return bad_request_response("Please enter Expiration Date.")
			if 'amount' not in param or param['amount'] == "" or param['amount'] is None:
				return bad_request_response("Please enter Amount.")
			if 'cvc' not in param or param['cvc'] =="" or param['cvc'] is  None:
				cvc=""
			else:
				cvc=None
			date_obj = datetime.strptime(param['expiry_date'], '%m/%y') 
			if date_obj.year == current_date.year:
				if date_obj.month < current_date.month:
					return bad_request_response("Your Card has expired")
			elif date_obj.year < current_date.year:
				return bad_request_response("Your Card has expired")
			try:
				count = 0
				if param['amount'] <=20:
					print("cheap")
					payment_obj = CheapPaymentGateway(param['card_number'],param['card_holder'],date_obj.month,date_obj.year,param['amount'],cvc)
					payment_obj = payment_obj.paymentIntent()
				elif param['amount']>=21 and param['amount']<=500:
					print("Expensive")
					payment_obj = ExpensivePaymentGateway(param['card_number'],param['card_holder'],date_obj.month,date_obj.year,param['amount'],cvc)
					payment_obj = payment_obj.paymentIntent()
					if not payment_obj['status_action']:
						print("cheap")
						payment_obj = CheapPaymentGateway(param['card_number'],param['card_holder'],date_obj.month,date_obj.year,param['amount'],cvc)
						payment_obj = payment_obj.paymentIntent()
				else:
					print("premium")	
					payment_obj = PremiumPaymentGateway(param['card_number'],param['card_holder'],date_obj.month,date_obj.year,param['amount'],cvc)
					payment_obj = payment_obj.paymentIntent()
					if not payment_obj['status_action']:
						while count<=3:
							print("premium",count)
							count +=1
							payment_obj = PremiumPaymentGateway(param['card_number'],param['card_holder'],date_obj.month,date_obj.year,param['amount'],cvc)
							payment_obj = payment_obj.paymentIntent()
							if payment_obj['status_action']:
								break;
				if payment_obj['status_action']:
					context = {
						"success": {"message": "Payment Successfully."},
						"status": True,
						"data": payment_obj['data'],
						"code": 200
					}
					return jsonify(context)
				else:
					context = {
						"success": {"message": payment_obj['message']},
						"status": payment_obj['status'],
						"code": payment_obj['code'],
						"parameter": payment_obj['parameter']
					}
					return jsonify(context)
			except Exception as e:
				return bad_request_response(e.__str__())

		except Exception as e:
			return bad_request_response(e.__str__())
app.add_url_rule("/api/payment",view_func=ProcessPayment.as_view('payment'))