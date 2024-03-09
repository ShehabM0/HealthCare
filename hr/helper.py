from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from random import randrange

def SendEmail(userName, userEmail, userPass):
    subject, from_email= "Congratulations, Your email is ready!", settings.EMAIL_HOST_USER
    text_content = "message."
    html_content = f"<div style=\"padding:25px; border: 1px solid black\"><h1 style=\"font-family: monospace; text-align: center\">Health Care</h1><p style=\"font-family: monospace;font-size: 15px;text-align: left;line-height: 2\">Hi {userName},<br>I wanted to take a moment and acknowledge the successful setup of your email account.<br><br>I understand that navigating new systems can be challenging, and I am impressed with your ability to complete the necessary information This reflects positively on your adaptability and technical skills.<br><br>Having your email up and running smoothly ensures you can stay connected with colleagues, access important information, and fulfill your role effectively.<br><br>Welcome to the hospital team, and please don't hesitate to reach out to me if you have any questions about your email account or other technical support needs.<br><br><p style=\"font-family: monospace;font-weight: bold;text-align: center;font-size: 16px;line-height: 2\">Email: {userEmail}<br>Password: {userPass}</p>Best regards,<br>HealthCare HR.</p></div>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [userEmail])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()
    return result

def GenerateRandomPass(str, n):
    for i in range(n):
        str += f"{randrange(10)}"
    return str
