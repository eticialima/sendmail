from django.urls import path 
from . import views

urlpatterns = [ 
    path('', views.OptionsView.as_view(), name='options-view'), 

	path('hooks/', views.SendmailHooksListView.as_view(), name='hooks-list'), 
	path('hooks-create/', views.SendmailHooksCreate.as_view(), name='hooks-create'),
	# path('<int:pk>/update/',SendmailHooksUpdate.as_view(), name='hooks-update'),
	# path('<int:pk>/delete/', SendmailHooksDelete.as_view(), name='hooks-delete'), 
 
    path('pdf/', views.SendmailPdfList.as_view(), name='pdf-list'), 
	path('pdf-create/', views.SendmailPdfCreate.as_view(), name='pdf-create'), 
	# path('<int:pk>/update/', SendmailPdfUpdate.as_view(), name='update'),
	# path('<int:pk>/delete/',  SendmailPdfDelete.as_view(), name='delete'),
    
    path('contato/', views.contato, name='contato'),
  
  
]