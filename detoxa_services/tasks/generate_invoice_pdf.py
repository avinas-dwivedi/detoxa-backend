import requests
import os

from datetime import datetime
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

from detoxa_services.models.orders import Order
from detoxa_services.models.transactions_models import Invoice, OrderTransaction
from detoxa_services.models.users import Users
from detoxa_services.utils.generate_invoice import generate_pdf


@shared_task
def generate_invoice(user, order_id):
    """
    Generate Invoice pdf
    """
    pdf_url = generate_pdf(user,order_id)
    invoice_number = f'OD{datetime.now().strftime("%Y%m%d")}{order_id}'
    print(invoice_number)
    invoice_obj = Invoice.objects.create(user=Users.objects.get(id=user), order=OrderTransaction.objects.get(
        order__id=order_id), invoice_number=invoice_number, invoice_amount=Order.objects.get(id=order_id).order_total, invoice_url=pdf_url)
    print('invoice_obj',invoice_obj)
    try:
        file_path = requests.get(pdf_url)
        print('file_path',file_path)
        file_name = '{}.pdf'.format(invoice_obj.invoice_number)
        print('file_name',file_name)
        with open(file_name, 'wb') as output:
            output.write(file_path.content)
        file_location = (os.path.abspath(file_name))
        print('file_location',file_location)
        mail = EmailMessage('Invoice for order on detoxa','Hi,<br> Please find below the attached invoice for your refernce.', settings.FROM_EMAIL, [Users.objects.get(id=user).email])
        mail.content_subtype = "html"
        mail.attach_file(file_name)
        mail.send()
        print('mail sent')
        if os.path.exists(file_location):
            os.remove(file_location)
    except Exception as e:
        print('Exception:', e)
    return 'Invoice for order id {}'.format(order_id)
