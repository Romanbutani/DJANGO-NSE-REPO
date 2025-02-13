import csv
from .models import QuoteData

def check_for_existing_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Check if this entry already exists in the database
            if QuoteData.objects.filter(
                date=row['date'],
                expiry_date=row['expiry_date'],
                option_type=row['option_type'],
            ).exists():
                return True

    return False
