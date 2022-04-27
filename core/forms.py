from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from .models import SendmailHooks, SendmailPdf
from django.conf import settings

# Forms do Revisão Manual
class SendmailHooksForm(forms.ModelForm):
    class Meta:
        model = SendmailHooks
        fields = '__all__' 
        
    def __init__(self,user=None, *args, **kwargs):
        super(SendmailHooksForm, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'  
	
        
class SendmailPdfForm(forms.ModelForm):
    class Meta:
        model = SendmailPdf
        fields = '__all__' 
    
    def __init__(self,user=None, *args, **kwargs):
        super(SendmailPdfForm, self).__init__(*args, **kwargs)   
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'  
	
         
# modelos do formulario de contato
class ContatoForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.CharField(label='Subject', max_length=120)
    message = forms.CharField(label='Message', widget=forms.Textarea())
 
    # funcao que envia email send_mail
    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        email_template = """
        Dear {name}
        Here is the text version of the email from template
        """
        
        html_string = render_to_string('simple/sendmail.html') 
        html_template = html_string.replace('{', '{{').replace('}', '}}').replace('{{$', '{').replace('$}}', '}')
        
        email_context = {
            'name': name, 
            'email': email, 
            'subject': subject,
            'message': message,
        }
        body = email_template.format(**email_context)
        html_body = html_template.format(**email_context)
        
        # send_mail é core mail do django
        send_mail(
            "teste", 
            body, 
            settings.EMAIL_HOST_USER,
            [email], 
            html_message = html_body
        )
    
   