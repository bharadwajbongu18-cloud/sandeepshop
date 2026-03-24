from django.urls import path
from .views import home, process_qr, export_excel

urlpatterns = [
    path('', home, name='home'),
    path('process/', process_qr, name='process_qr'),
    path('export/', export_excel, name='export_excel'),
]