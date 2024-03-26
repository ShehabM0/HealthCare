from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from random import randrange

SUBJECTS = {
    "hr_account_creation.html": "Congratulations, Your email is ready!",
    "registration.html": "Your SignUp verification code",
    "change_email.html": "Your Email verification code"
}

def SendEmail(userName, userEmail, userPass, code, expire_time, htmlFile):
    subject = SUBJECTS[htmlFile]
    text_content = "Email Body."
    from_email = settings.EMAIL_HOST_USER

    html_file = get_template(htmlFile)
    html_content = html_file.render({
        "user_name": userName,
        "user_email": userEmail,
        "user_password": userPass,
        "code": code,
        "expire_time": expire_time
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [userEmail])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return result

def GenerateRandomPass(str, n):
    for i in range(n):
        str += f"{randrange(10)}"
    return str
