import pandas as pd
from celery import shared_task
from .models import QuoteData
import os

@shared_task
def process_csv(file_path):
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
        df.columns = df.columns.str.strip().str.upper()  

        if df.empty:
            print("The CSV file is empty")
            return "The CSV file is empty"

        print(df.head())  
        df['STRIKE PRICE'] = df['STRIKE PRICE'].apply(lambda x: '0' if x == '-' else x)
        df['STRIKE PRICE'] = pd.to_numeric(df['STRIKE PRICE'], errors='coerce')  
        
        # Handle other columns where numeric values are expected but may contain '-' or commas
        columns_to_clean = ['OPEN PRICE', 'HIGH PRICE', 'LOW PRICE', 'CLOSE PRICE', 
                            'LAST PRICE', 'SETTLE PRICE', 'VOLUME', 'VALUE', 'PREMIUM VALUE', 
                            'OPEN INTEREST', 'CHANGE IN OI']
        
        for col in columns_to_clean:
            df[col] = df[col].apply(lambda x: '0' if x == '-' else x)  
            df[col] = df[col].replace({',': ''}, regex=True)  
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)

        data_to_insert = []
        for _, row in df.iterrows():
            try:
                data_to_insert.append(QuoteData(
                    date=pd.to_datetime(row['DATE'], dayfirst=True).date(),
                    expiry_date=pd.to_datetime(row['EXPIRY DATE'], dayfirst=True).date(),
                    option_type=row['OPTION TYPE'],
                    strike_price=row['STRIKE PRICE'] if pd.notna(row['STRIKE PRICE']) else None,
                    open_price=row['OPEN PRICE'],
                    high_price=row['HIGH PRICE'],
                    low_price=row['LOW PRICE'],
                    close_price=row['CLOSE PRICE'],
                    last_price=row['LAST PRICE'],
                    settle_price=row['SETTLE PRICE'],
                    volume=int(row['VOLUME']),
                    value=row['VALUE'],
                    premium_value=row['PREMIUM VALUE'],
                    open_interest=int(row['OPEN INTEREST']),
                    change_in_oi=int(row['CHANGE IN OI'])
                ))
            except Exception as e:
                print(f"Skipping row due to error: {e}")  

        if not data_to_insert:
            print("No data to insert")
            return "No data extracted from CSV"

        QuoteData.objects.bulk_create(data_to_insert, batch_size=500)

        if os.path.exists(file_path):
            os.remove(file_path)

        print("CSV file processed successfully")
        return "CSV file processed successfully"

    except Exception as e:
        print("Error processing CSV:", e)
        return str(e)
