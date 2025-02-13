from django.urls import path
from .views import upload_csv,csv_data_list  

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('data_list/', csv_data_list, name='csv_data_list'),  
]
