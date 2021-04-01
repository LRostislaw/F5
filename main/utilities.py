from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.signing import Signer
from F5.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        pass
    host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)

    user.email_user(subject, body_text)


def send_choice_notification(user, username, email):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        pass
    host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': username, 'email': email}
    subject = render_to_string('email/choice_doctor_subject.txt', context)
    body_text = render_to_string('email/choice_doctor_body.txt', context)

    send_mail(subject, body_text, email, [email])