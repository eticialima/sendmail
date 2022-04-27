from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string 
from django.core.mail import EmailMultiAlternatives  
from weasyprint import HTML     
import weasyprint
 
class SendmailHooks(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100) 
    subject = models.TextField(max_length=200, null=True, blank=True)

email_template = """
Usuario: {name} Email: {email}
""" 
html_string = render_to_string('hooks/email_template.html')
html_template = html_string.replace('{', '{{').replace('}', '}}').replace('{{$', '{').replace('$}}', '}')

@receiver(post_save, sender=SendmailHooks)
def post_save_handler(sender, **kwargs):
    send = kwargs.get('instance', None)
    created = kwargs.get('created', False)
    raw = kwargs.get('raw', False)
    email_context = {
        'name': send.name, 
        'email': send.email,
        'subject': send.subject
    }
    email_body = email_template.format(**email_context)
    html_body = html_template.format(**email_context)  
   
    send_mail(
        'Email - Django sendmail hooks', email_body, 
        settings.EMAIL_HOST_USER, [email_context['email']], 
        html_message = html_body, 
        fail_silently=False
    ) 

 
# SendMail with pdf file 
class SendmailPdf(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100) 
    sexo = models.CharField('sexo', max_length=1, choices=[('1','Feminino'),('2','Masculino')])

   
@receiver(post_save, sender=SendmailPdf)
def post_save_handler(sender, **kwargs):
    sendemail = kwargs.get('instance', None)
    created = kwargs.get('created', False)
    raw = kwargs.get('raw', False)
 
    # Configuração do body do email
    email_template = """
    Usuario: {name} Email: {email}
    Geramos um pdf.
    """ 
    html_string = render_to_string('pdf/html_template_email.html') 
    html_body = <a href="{% url 'hooks-create' %}">Sendmail With Hooks</a> 
html_string.replace('{', '{{').replace('}', '}}').replace('{{$', '{').replace('$}}', '}')

    email_context = {
        'name': sendemail.name, 
        'email': sendemail.email, 
        'sexo': sendemail.sexo
    }

    # converter html para pdf
    html_string = render_to_string('pdf/html_template_email.html',{'user': email_context})
    html_template = html_string.replace('{', '{{').replace('}', '}}').replace('{{$', '{').replace('$}}', '}')
 
    response = HttpResponse(content_type='application/pdf')
    pdf = html_template.format(**email_context)
    
    # html para pdf
    response['Content-Disposition'] = 'filename=certificate_{}'.format(email_context['name']) + '.pdf'
    pdf = weasyprint.HTML(string=pdf, base_url='http://127.0.0.1:8000/media').write_pdf(stylesheets=[weasyprint.CSS(string='body { font-family: serif}')]) 
 
    template_body = email_template.format(**email_context) 
    html_body = html_body.format(**email_context)

    to_emails = [str(email_context['email'])]
    subject = "test pdf"

    email = EmailMultiAlternatives(subject, body=template_body, from_email=settings.EMAIL_HOST_USER, to=to_emails )
    email.attach("emailpdf_{}".format(email_context['name']) + '.pdf', pdf, "application/pdf")
    email.attach_alternative(html_body, "text/html")
    email.content_subtype = "pdf"  
    email.decode = 'us-ascii' 
    email.send()  