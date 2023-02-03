import razorpay
import requests
import simplejson
from ..models.transactions_models import Transactions
from ..serializers.transaction_serializers import TransactionSerializer, UpdateTransactionSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from detoxa_services.utils.user_authentication import UserAuthentication
from ..constants import payment_constants
from datetime import datetime, timedelta


def createRazorPayOrder(amount):
    data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    }

    response = requests.post(payment_constants.razorpay_endpoint + payment_constants.create_order,
                             data=simplejson.dumps(data),
                             headers=payment_constants.headers, auth=payment_constants.razorpay_auth)

    return response


class CreateSubscriptionTransaction(CreateAPIView):
    """
    This class is used to create a new transaction for a subscription
    """
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        """
        This method is used to create a new transaction for a subscription plan
        """
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            # Convert Amount from Rs to Paisa
            amount = int(amount) * 100
            amount = int(amount)
            tenure = serializer.validated_data['tenure']
            if tenure == "1":
                days = 30
            elif tenure == "6":
                days = 120
            else:
                days = 365
            response = createRazorPayOrder(int(amount))
            if response.status_code == 200:
                razorpay_order_id = response.json().get('id')

                # Inactive old transaction for now.
                Transactions.objects.filter(user=logged_in_user).update(is_active=False)
                # Create Entry in Transactions Table
                transaction_obj = Transactions.objects.create(
                    user=logged_in_user,
                    tenure=serializer.validated_data['tenure'],
                    subscription_type=serializer.validated_data['subscription_type'],
                    amount=serializer.validated_data['amount'],
                    order_id=razorpay_order_id,
                    status="Pending",
                    transaction_datetime=datetime.now(),
                    subscription_start_date=datetime.now(),
                    subscription_end_date=datetime.now() + timedelta(
                        days=days)
                )
                transaction_obj_dict = {'id': transaction_obj.id}
                transaction_obj_dict.update(serializer.data)
                if transaction_obj:
                    # "response": response,
                    return Response(
                        {"result": True, "detail": {"razorpay_order_id": razorpay_order_id, "status": 'Success',
                                                    "transaction_dict": transaction_obj_dict}},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"result": False, "detail": "Error while saving the entries"},
                        status=status.HTTP_400_BAD_REQUEST)
                # return Response(transaction_obj_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSubscriptionTransaction(CreateAPIView):
    """
    This class is used to update a transaction for a subscription
    """
    serializer_class = UpdateTransactionSerializer

    def post(self, request, *args, **kwargs):
        """
        This method is used to update transaction for a subscription plan
        """
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        serializer = UpdateTransactionSerializer(data=request.data)
        if serializer.is_valid():
            payment_id = serializer.validated_data['payment_id']
            order_id = serializer.validated_data['order_id']
            signature = serializer.validated_data['signature']
            # fetch Entry from Transactions Table
            transaction_obj = Transactions.objects.filter(
                user=logged_in_user, order_id=order_id, is_active=True).first()
            if transaction_obj:
                data = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }

                client = razorpay.Client(auth=payment_constants.razorpay_auth)

                # checking if the transaction is valid or not if it is "valid" then check will return None
                check = client.utility.verify_payment_signature(data)

                if check is not None:
                    return Response({'error': 'Something went wrong'})
                else:
                    # if payment is successful that means check is None then we will turn isPaid=True
                    transaction_obj.payment_id = payment_id
                    transaction_obj.signature = signature
                    transaction_obj.status = "Success"
                    transaction_obj.save()

                    return Response({"result": True}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"result": False, "detail": "Error while fetching the entries"},
                    status=status.HTTP_400_BAD_REQUEST)
                # return Response(transaction_obj_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
