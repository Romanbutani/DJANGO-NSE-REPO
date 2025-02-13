import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from .models import QuoteData
from .tasks import process_csv
from .utils import check_for_existing_data

# View to handle CSV file upload
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        if not file.name.endswith('.csv'):
            raise SuspiciousOperation("Only CSV files are allowed.")
        
        custom_directory = os.path.join(settings.BASE_DIR, 'csv_file')  

        # Check if the folder exists; if not, create it
        if not os.path.exists(custom_directory):
            os.makedirs(custom_directory)

        # Get the full file path
        file_path = os.path.join(custom_directory, file.name)

        # Save the file in the custom folder
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if check_for_existing_data(file_path):
                return render(request, 'upload.html', {'error': 'This CSV data is already uploaded.'})        

            process_csv.delay(file_path)

        except Exception as e:
            # Handle errors if file saving fails
            print(f"Error saving file: {e}")
            return render(request, 'upload.html', {'error': 'File could not be saved.'})

        # Redirect to csv_data_list view after upload
        return redirect('csv_data_list')  
    return render(request, 'upload.html')  

# View to display the uploaded CSV data
def csv_data_list(request):
    data = QuoteData.objects.all()
    print("data",data)
    return render(request, 'data_list.html', {'data': data})
