from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from django.views.generic.base import TemplateView  
from django.shortcuts import render
from .models import SendmailHooks, SendmailPdf
from .forms import SendmailHooksForm, SendmailPdfForm, ContatoForm

class OptionsView(TemplateView):
	template_name = 'base/_base.html'

# Sendmail simple
def contato(request):
    form = ContatoForm(request.POST or None) 
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail() 
            messages.success(request, 'Email successfully sent!')
            form = ContatoForm() 
        else:
            messages.error(request, 'Email error sent!')
    context = {'form': form}
    return render(request, 'simple/contato.html', context)


# Sendmail with Hooks
class SendmailHooksCreate(CreateView):
	template_name = 'hooks/email_form.html'
	form_class = SendmailHooksForm
	success_url = reverse_lazy('hooks-list')
	success_message = 'Email successfully sent!'  
  
class SendmailHooksListView(ListView):
	model = SendmailHooks
	template_name = 'hooks/email_list.html' 
 

#SendMail with pfd File in anexo
class SendmailPdfCreate(CreateView):
	template_name = 'pdf/pdf_form.html'
	form_class = SendmailPdfForm
	success_url = reverse_lazy('pdf-list')
	success_message = 'Email successfully sent!' 

class SendmailPdfList(ListView):
	model = SendmailPdf
	template_name = 'pdf/pdf_list.html' 