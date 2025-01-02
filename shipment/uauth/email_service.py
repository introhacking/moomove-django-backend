from django.core.mail import send_mail
import requests
import random
import smtplib
from email.message import EmailMessage
from django.conf import settings

from .models import User
from email.message import EmailMessage 


# def send_email(subject,to_email="",to_candidate="",html_body="",plain_text="",recipients=[]):
#     msg=EmailMessage()
#     msg['Subject']=subject
#     msg['From']='adminbot@augtrans.com'
#     if recipients:
#         msg['To']=recipients
#     else:
#         msg['To']=to_email
#     msg.set_content(plain_text)
#     if html_body:
#         msg.add_alternative(html_body,subtype='html')
#     mailserver = smtplib.SMTP('smtp.office365.com',587)
#     mailserver.ehlo()
#     mailserver.starttls()
#     mailserver.login('adminbot@augtrans.com','Orbit@2022')
#     mailserver.send_message(msg)
#     mailserver.quit()

def send_email(subject, to_email="", to_candidate="", html_body="", plain_text="", recipients=[]):

        
    # Authentication information
    app_id = '1d83ca1e-9aa2-4072-a93c-91366891f305'  
    client_secret = 'vOT8Q~1Az1PHHx3ifE7o6_PnNij-ql5O6KAxwanI'
    tenant_id = '323bd849-9700-48fc-a12e-fd204620ebe2'
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    user_obj_id = '915a80c8-bf3b-4d46-920e-9ff49d321d4a'
    # Get access token
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': client_secret,
        'resource': 'https://graph.microsoft.com',
    }
    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get('access_token')
    
    # Send email
    email_url = f'https://graph.microsoft.com/v1.0/users/{user_obj_id}/sendMail'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    email_data = {
        'message': {
            'subject': subject,
            'body': {
                'contentType': 'HTML',
                'content': html_body
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': to_email
                    }
                }
            ]
        },
        'saveToSentItems': 'true'
    }
    
    response = requests.post(email_url.format(user_id=user_obj_id), headers=headers, json=email_data)
    
    if response.status_code == 202:
        print('Email sent successfully.')
    else:
        print('Failed to send email.')
        print(response.json())


def send_opt_via_email(email):
    otp= random.randint(1000,9999)
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
    send_email(
        subject="Email verification OTP",
         html_body=f'Your verification OTP is {otp}',
        to_email=email
    )

def send_rgain_via_email(email):
    user_obj = User.objects.get(email=email)
    
    # Construct the URL
    #reset_url = "https://csm.augtrans.com:8226/auth/sign-in"
    reset_url = "http://testmoomoveui.s3-website.ap-south-1.amazonaws.com/"

    # Email body
    email_body = f"""
        <p>Dear Team,</p>

        <p>Thank you for registering with <strong>“Moomove!”</strong> We are thrilled to have you on board.</p>

        <p>Our platform simplifies your shipping process by offering a range of cards from various companies, enabling you to select the best option and generate quotations effortlessly.</p>

        <p>We are here to make your logistics journey smoother, faster, and more efficient. If you have any questions or need support, feel free to reach out to us.</p>
        
        <p>To ensure secure access to Moomove, please take a moment to reset your password. Follow these steps:</p>
        <ul>
            <li>Go to the Moomove login page.</li>
            <li>Click on <a href="{reset_url}">Click here to regain your password</a> and follow the instructions to create a new password.</li>
        </ul>

        <p>If you have any questions or need assistance, please do not hesitate to contact the System .</p>
    """

    send_email(
        subject="Welcome To Moomove",
        html_body=email_body,
        to_email=email
    )

# def send_token_via_email(email):
#     if User.objects.filter(email=email).exists():
#         user = User.objects.get(email = email)
#         uid = urlsafe_base64_encode(force_bytes(user.id))
#         print('Encoded UID', uid)
#         token = PasswordResetTokenGenerator().make_token(user)

def send_opt_via_whatsapp(mobile_number):
    pass


