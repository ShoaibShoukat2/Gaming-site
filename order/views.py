import logging
import json
import requests
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle





# Configure logging
logger = logging.getLogger(__name__)

''' Khalti integrations '''
def initkhalti(request):
    url = "https://khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    website_url = request.POST.get('website_url')  
    amount = request.POST.get('amount')
    purchase_order_id = request.POST.get('purchase_order_id')

    logger.debug("initkhalti: URL: %s", url)
    logger.debug("initkhalti: Return URL: %s", return_url)
    logger.debug("initkhalti: Website URL: %s", website_url)
    logger.debug("initkhalti: Amount: %s", amount)
    logger.debug("initkhalti: Purchase Order ID: %s", purchase_order_id)

    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
            "name": "Bibek Dahal",
            "email": "test@khalti.com",
            "phone": "9800000001"
        }
    })


    headers = {
        'Authorization': 'Key live_secret_key_70714e54015141c682d6b88608067f87',  
        'Content-Type': 'application/json',
    }


    try:
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        logger.debug("initkhalti: Response: %s", response_data)

        if response.status_code == 200 and 'payment_url' in response_data:
            return redirect(response_data['payment_url'])
        else:
            messages.warning(request, "Failed to initiate payment.")
            logger.warning("Failed to initiate payment. Response: %s", response_data)
    except requests.RequestException as e:
        messages.error(request, f"An error occurred: {e}")
        logger.error("RequestException: %s", e)

    return redirect("home")





@login_required
def order(request):
    if request.method == "POST":
        user = request.user
        logger.info("Order request received.")

        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_instance = order_form.save(commit=False)
            order_instance.user = user

            # Extract form data
            return_url = request.POST.get('return_url')
            website_url = request.POST.get('website_url')
            service_id = request.POST.get('service')
            gateway_id = request.POST.get('gateway')
            promo_code_input = request.POST.get('promo_code')

            # Fetch the product
            try:
                product = ProductItem.objects.get(id=service_id)
            except ProductItem.DoesNotExist:
                messages.warning(request, "Product or Payment Gateway not found.")
                return redirect('frontend:index')

            # Calculate the initial amount
            amount = product.item_price

            # Initialize discounted amount
            discounted_amount = amount
            logger.info(f"Original Price: {amount}")

            # Validate and apply the promo code
            if promo_code_input:
                try:
                    promo_code = PromoCode.objects.get(code=promo_code_input)

                    # Ensure promo code is either user-specific or general
                    if promo_code.user and promo_code.user != user:
                        messages.warning(request, "This promo code is not valid for your account.")
                        return redirect(request.path)  # Redirect back to the same page

                    elif promo_code.is_valid():
                        discounted_amount = promo_code.apply_discount(discounted_amount)
                        logger.info(f"Promo code '{promo_code_input}' applied. Discounted Price: {discounted_amount}")
                    else:
                        messages.warning(request, "Promo code is invalid or expired.")
                        return redirect(request.path)  # Redirect back to the same page

                except PromoCode.DoesNotExist:
                    messages.warning(request, "Invalid promo code.")
                    return redirect(request.path)  # Redirect back to the same page
            else:
                logger.info("No promo code provided.")
                
            
                


            # Validate required fields
            if not all([return_url, website_url, discounted_amount]):
                logger.warning("Missing required payment details.")
                messages.warning(request, "Missing required payment details.")
                return redirect('frontend:index')

            # Save data based on the product type
            if product.item_name == "Gpt":
                order_instance.chatgpt_login_email = request.POST.get('gptField1')
                order_instance.chatgpt_login_password = request.POST.get('gptField2')
                logger.debug(f"GPT Data Saved: Email={order_instance.chatgpt_login_email}, Password={order_instance.chatgpt_login_password}")

            elif product.item_name == "Truecaller Premium":
                order_instance.truecaller_number = request.POST.get('truecallerNumber')
                order_instance.password_optional = request.POST.get('truecallerPassword')
                logger.debug(f"Truecaller Data Saved: Number={order_instance.truecaller_number}, Password={order_instance.password_optional}")

            elif product.item_name == "Udemy Course":
                order_instance.udemy_course_url = request.POST.get('udemyCourseUrl')
                order_instance.udemy_account_email = request.POST.get('udemyAccountEmail')
                logger.debug(f"Udemy Data Saved: Course URL={order_instance.udemy_course_url}, Email={order_instance.udemy_account_email}")

            # Save the order instance and get its ID
            order_instance.totalPrice = discounted_amount  # Save the final price
            order_instance.save()
            purchase_order_id = order_instance.id
            logger.debug(f"Order instance created with ID: {purchase_order_id}")

            # Prepare the payload for payment gateway
            full_name = user.name or "Anonymous"
            email = user.email or "test@khalti.com"
            payload = {
                "return_url": return_url,
                "website_url": website_url,
                "amount": int(discounted_amount * 100),  # Convert to the smallest currency unit
                "purchase_order_id": purchase_order_id,
                "purchase_order_name": product.item_name,
                "customer_info": {
                    "name": full_name,
                    "email": email,
                    "phone": user.phone_no or "92342342"
                }
            }

            # Add product-specific data to the payload
            if product.item_name == "Gpt":
                payload['gpt_email'] = order_instance.chatgpt_login_email
                payload['gpt_password'] = order_instance.chatgpt_login_password
            elif product.item_name == "Truecaller Premium":
                payload['truecaller_number'] = order_instance.truecaller_number
                payload['truecaller_password'] = order_instance.password_optional
            elif product.item_name == "Udemy Course":
                payload['udemy_course_url'] = order_instance.udemy_course_url
                payload['udemy_account_email'] = order_instance.udemy_account_email

            # Send request to the payment gateway
            headers = {
                'Authorization': 'Key live_secret_key_70714e54015141c682d6b88608067f87',  # Secret key
                'Content-Type': 'application/json',
            }
            try:
                response = requests.post("https://khalti.com/api/v2/epayment/initiate/", headers=headers, data=json.dumps(payload))
                logger.debug(f"Payment gateway response status: {response.status_code}")
                logger.debug(f"Payment gateway response content: {response.text}")

                response_data = response.json()
                if response.status_code == 200 and 'payment_url' in response_data:
                    return redirect(response_data['payment_url'])
                else:
                    logger.warning(f"Failed to initiate payment. Response data: {response_data}")
                    messages.warning(request, "Failed to initiate payment.")
            except requests.RequestException as e:
                logger.error(f"An error occurred during payment initiation: {e}")
                messages.error(request, f"An error occurred: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                messages.error(request, f"An unexpected error occurred: {e}")

            # If order was successfully placed but payment initiation failed
            messages.success(request, "Order placed successfully!")
            return redirect('frontend:index')
        else:
            logger.warning(f"Order form errors: {order_form.errors}")
            messages.warning(request, order_form.errors)
            return redirect('frontend:index')

    else:
        return redirect('frontend:index')
    
    

    
    

def generate_invoice(order):
    """Generate a detailed and professional PDF invoice for the given order."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create a canvas for drawing
    p = canvas.Canvas(buffer, pagesize=letter)
    
    width, height = letter

    # Add company logo
    p.drawImage('C:/Users/Shoaib/Downloads/gaming/gaming/order/static/logo.png', 50, height - 100, width=150, height=50)

    
    # Invoice Header
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 150, "Invoice")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 175, f"Order Number: {order.id}")
    p.drawString(50, height - 195, f"Order Date: {order.created.strftime('%Y-%m-%d')}")
    p.drawString(50, height - 215, f"Total Amount: ${order.totalPrice:.2f}")

    # Add a line for separation
    p.line(50, height - 230, width - 50, height - 230)

    # Add product details in a table
    data = [["Product Name", "Item Name", "Price"]]
    product = order.product
    product_item = order.product_item
    data.append([product.product_name, product_item.item_name if product_item else 'N/A', f"${product_item.item_price if product_item else 'N/A':.2f}"])

    table = Table(data, colWidths=[200, 200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table)

    # Add more sections as needed
    p.drawString(50, height - 300, "Thank you for your order!")
    p.drawString(50, height - 320, "For any questions, contact us at contact@company.com")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer




















def send_invoice_email(order):
    """Send the invoice PDF and detailed email to the user."""
    # Generate the PDF invoice
    pdf_buffer = generate_invoice(order)

    # Email subject and message
    subject = 'Your Order Has Been Received and Is Processing!'
    message = f"""
    Dear {order.user.name},
    
    Thank you for your order! We’re excited to let you know that it has been received and is currently being processed.

    Order Details:
    
    Order Number: {order.id}
    Order Date: {order.created.strftime('%Y-%m-%d')}
    Product: {order.product.product_name}  # Access product name
    Item: {order.product_item.item_name if order.product_item else 'N/A'}  

    You will receive another email with access instructions once your order is ready.

    If you have any questions or need assistance in the meantime, please don’t hesitate to reach out.

    Thank you for choosing us!

    Best regards,
    hamrosubscription.com
    """

    # Prepare email
    email = EmailMessage(
        subject,
        message,
        'orderdelivery@hamrosubscription.com', 
        [order.user.email],  
    )


    # Attach PDF receipt
    email.attach("Receipt.pdf", pdf_buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()
    
    
    notify_new_order(order)
    
    

def notify_new_order(order):
    """Send a notification email to admin when a new order is received."""
    # Email subject and message for the admin notification
    subject = 'New Order Received!'
    message = f"""
    A new order has been placed on hamrosubscription.com.

    Order Details:
    
    Order Number: {order.id}
    Customer Name: {order.user.name}
    Order Date: {order.created.strftime('%Y-%m-%d')}
    Product: {order.product.product_name}
    Item: {order.product_item.item_name if order.product_item else 'N/A'}

    Please log in to the admin panel to review the order details.
    """

    # Prepare email to notify admin
    admin_email = EmailMessage(
        subject,
        message,
        'orderdelivery@hamrosubscription.com', 
        ['admin@hamrosubscription.com'],  
    )

    # Send the notification email
    admin_email.send()






def notify_new_order(order):
    """Send a notification email to admin when a new order is received."""
    # Email subject and message for the admin notification
    subject = 'New Order Received!'
    message = f"""
    A new order has been placed on hamrosubscription.com.

    Order Details:
    
    Order Number: {order.id}
    Customer Name: {order.user.name}
    Order Date: {order.created.strftime('%Y-%m-%d')}
    Product: {order.product.product_name}
    Item: {order.product_item.item_name if order.product_item else 'N/A'}

    Please log in to the admin panel to review the order details.
    """

    # Prepare email to notify admin
    admin_email = EmailMessage(
        subject,
        message,
        'orderdelivery@hamrosubscription.com',  
        ['admin@hamrosubscription.com'],  
    )

    # Send the notification email
    admin_email.send()
    



  
    
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'Key 1f3f3e847f1a4c19b48506f4c590bd2e',  # Secret key
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        purchase_order_id = request.GET.get('purchase_order_id')  # Get the purchase order ID from the request
        
        data = json.dumps({
            'pidx': pidx
        })
        
            
        
        try:
            # Send request to Khalti
            res = requests.post(url, headers=headers, data=data)
            response_data = res.json()
            print("verifyKhalti: Response:", response_data)

            if response_data.get('status') == 'Completed':
                print("Payment completed")
                
                # Fetch the order using purchase_order_id, not pidx
                try:
                    order = Order.objects.get(id=purchase_order_id)
                    order.order_status = 'success'
                    order.transaction_id = response_data.get('transaction_id')
                    order.save()
                    print("Order Saved")

                    # Send the invoice to the user
                    send_invoice_email(order)

                except ObjectDoesNotExist:
                    logger.error(f"Order with ID {purchase_order_id} not found")
                    return redirect('/error_page')  # Handle order not found

            else:
                logger.warning("Payment not completed: %s", response_data)

        except requests.RequestException as e:
            logger.error("RequestException: %s", e)
        except Exception as e:
            logger.error("Unexpected error: %s", e)

    return redirect('/')





