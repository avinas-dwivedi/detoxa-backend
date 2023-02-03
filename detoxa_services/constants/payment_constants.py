import os

razorpay_endpoint = 'https://api.razorpay.com/v1'
headers = {'content-type': 'application/json'}
razorpay_key_id = os.getenv("RAZOR_PAY_KEY")
razorpay_key_secret = os.getenv("RAZOR_PAY_SECRET")
razorpay_auth = (razorpay_key_id, razorpay_key_secret)
create_order = '/orders'