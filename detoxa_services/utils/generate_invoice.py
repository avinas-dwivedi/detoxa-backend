import io
import os
import boto3
from datetime import datetime
from email.message import EmailMessage

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.colors import black,grey,lightgrey,whitesmoke
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings

import requests
from detoxa_services.models.kits_models import Kit
from detoxa_services.models.orders import Order
from detoxa_services.models.transactions_models import Invoice, OrderTransaction


def generate_pdf(user, order_id):
    """
    Generate Invoice pdf
    """
    pdf_url = None
    pdf_file_name = f'OD{datetime.now().strftime("%Y%m%d")}{order_id}'

    print(user,order_id)
    order = OrderTransaction.objects.get(order__id=order_id)
    # order = OrderTransaction.objects.filter(order__id=order_id)[0]
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFillColor(black)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(250, 760, 'TAX INVOICE')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,730,'Sold By: Shreyash Retail Private Limited')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,710,'Ship-from Address: ')
    c.setFont('Helvetica', 10)
    c.drawString(133,710,'Instakart Services Private Limited, Plot No A1, Haringhata Industrial Park, District Nadia, West Bengal')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,690,'GSTIN: ') 
    c.setFont('Helvetica', 12)
    c.drawString(65,690,'19AAXCS0655F1ZV')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,670,'FSSAI License No: ') 
    c.setFont('Helvetica', 12)
    c.drawString(130,670,'13321999000230')
    c.line(20, 640, 600, 640)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,620,'Order ID: ')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(75,620,f'{pdf_file_name}')  

    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,600,'Order Date: ')
    c.setFont('Helvetica', 12)
    c.drawString(85,600,f'{order.transaction_datetime.strftime("%d-%m-%Y")}')  

    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,580,'Invoice Date: ')
    c.setFont('Helvetica', 12)
    c.drawString(95,580,f'{order.transaction_datetime.strftime("%d-%m-%Y")}')

    c.setFont('Helvetica-Bold', 12) 
    c.drawString(20,560,'PAN: ')
    c.setFont('Helvetica', 12)
    c.drawString(50,560,'aaxcs0655f')  

    c.setFont('Helvetica-Bold', 12)
    c.drawString(20,540,'CIN: ')
    c.setFont('Helvetica', 12)
    c.drawString(45,540,'U52399DL2016PTC299716')  
    c.setFont('Helvetica', 10)
    c.drawString(20,510,f'Total Items: {len(order.order.order_items)}')
    c.setFont('Helvetica-Bold', 10)
    c.drawString(200,620,'Bill To: ')
    c.drawString(235,620,f'{order.order.user.full_name}')
    c.setFont('Helvetica-Bold', 10)
    c.drawString(400,620,'Ship To: ')
    c.setFont('Helvetica-Bold', 10)
    c.drawString(440,620,f'{order.order.user.full_name}')
    c.setFont('Helvetica', 10)
    c.drawString(200,610,f'{order.order.address.street}'+',')
    c.drawString(200,600,f'{order.order.address.city}'+'-')
    c.drawString(230,600,f'{order.order.address.pincode}'+',')
    c.drawString(200,590,f'{order.order.address.state}')
    c.setFont('Helvetica', 10)
    c.drawString(400,610,f'{order.order.address.street}'+',')
    c.drawString(400,600,f'{order.order.address.city}'+'-')
    c.drawString(430,600,f'{order.order.address.pincode}'+',')
    c.drawString(400,590,f'{order.order.address.state}')
    c.line(20, 500, 600, 500)
    item_list = []
    item_list.append(['S.NO','Name','Qty', 'Price','Discount', 'Taxable Value','IGST','Total'])
    item_count = 1
    qty = 0
    gross_amount = 0
    discount = 0
    taxable_value = 0
    igst = 0

    for order_item in order.order.order_items:
        kit_obj = Kit.objects.get(id=order.order.order_items[order_item]['id'])
        item_list.append([item_count,
                        kit_obj.name,
                        order.order.order_items[order_item]['quantity'],
                        float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price),
                        0,
                        (float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price))-0,
                        float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price)*0.18,
                        float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price)-float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price)*0.18
                        ]
                        )
        item_count+=1
        qty+=order.order.order_items[order_item]['quantity']
        gross_amount+=float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price)
        discount+=0
        taxable_value += (float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price))-discount
        igst += float(order.order.order_items[order_item]['quantity'])*float(kit_obj.price)*0.18
    item_list.append(['Total','',qty,gross_amount,discount,taxable_value,igst,float(order.order.order_total)])
    y_axis = 490-((len(order.order.order_items)+2)*0.25*inch)
    print(y_axis)
    t=Table(item_list,colWidths=[1* inch, 1*inch, 0.8* inch, 1* inch,  1* inch, 1.2* inch, 1* inch,  1* inch ],rowHeights= (len(order.order.order_items)+2)*[0.25*inch],hAlign='RIGHT') 
    t.setStyle(TableStyle([
    ('ALIGN',(1,1),(-2,-2),'LEFT'),
    ('FONT',(0,0),(-1,0),'Helvetica-Bold'), 
    ('ALIGN',(0,0),(0,-1),'LEFT'), 
    ('TEXTCOLOR',(0,0),(0,-1),black),
    ('TEXTCOLOR',(0,-1),(-1,-1),black),
    ('INNERGRID', (0,0), (-1,-1), 0.25, grey),
    ('BOX', (0,0), (-1,-1), 0.25, grey),
    ('SPAN',(0,len(item_list)-1),(1,len(item_list)-1)),
    ('ALIGN',(0,len(item_list)-1),(1,len(item_list)-1), 'RIGHT'),
    ('FONT',(0,len(item_list)-1),(1,len(item_list)-1), 'Helvetica-Bold'),
    ('ALIGN',(2,0),(-1,-1),'LEFT'),
       ]))
    data_len = len(item_list)
    for each in range(data_len):
        if each % 2 == 0:
            bg_color = lightgrey
        else:
            bg_color = whitesmoke
        t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
    t.wrap(0,0)
    t.drawOn(c, 20, y_axis)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(470,y_axis-50,f'Grand Total  {order.order.order_total}')
    c.setFont('Helvetica', 8)
    c.drawString(480,y_axis-60,f'Shreyash Retail Private Limited')
    c.setFont('Helvetica', 10)
    c.drawString(490,y_axis-200,f'Authorized Signatory')
    c.line(20, y_axis-210, 600, y_axis-210)
    c.showPage()
    c.save()
    buffer.seek(0)

    print(pdf_file_name)    
    with open(pdf_file_name, 'wb') as f:
        f.write(buffer.getvalue())
        buffer.close()
    s3 = boto3.resource('s3', region_name='us-east-2',
                    aws_access_key_id='AKIAZXI7ZAJGFBY52O7I',
                    aws_secret_access_key='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')
    s3.Bucket('detoxa').put_object(Key=pdf_file_name, Body=(
    open(pdf_file_name, 'rb')), ACL='public-read', ContentDisposition='inline')
    pdf_url = f'https://detoxa.s3.us-east-2.amazonaws.com/{pdf_file_name}'
    try:
        if pdf_file_name:
            os.remove(pdf_file_name)
    except:
        pass
    return pdf_url
