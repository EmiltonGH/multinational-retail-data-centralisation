import tabula
import jpype
import yaml
import sqlalchemy
from sqlalchemy import column
from sqlalchemy import create_engine, MetaData
import pandas as pd
from datetime import datetime
import requests
import boto3
from io import BytesIO

# You will use this class to connect with and upload data to the database.
class DatabaseConnector:
    # This will read the credentials yaml file and return a dictionary of the credentials.
    @staticmethod
    def read_db_creds(file_path):
        with open(file_path, 'r') as file:
            creds = yaml.safe_load(file)
        return creds
    
    # This will read the credentials from the return of read_db_creds method and initialise and return an sqlalchemy database engine
    @staticmethod
    def init_db_engine(file_path):
        credentials = DatabaseConnector.read_db_creds(file_path)
        db_url = f"postgresql://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}"
        
        engine = create_engine(db_url)
        return engine
    
    # To list all the tables in the database so you know which tables you can extract data from
    def list_db_tables(self, file_path):
        engine = self.init_db_engine(file_path)
        metadata = MetaData()
        metadata.bind = engine
        metadata.reflect(bind=engine)

        table_names = metadata.tables.keys()
        return table_names
    
    # This method will upload the table to the database
    def upload_to_db(self, file_path, df, table_name):
        engine = self.init_db_engine(file_path)
        
        # Convert DataFrame to SQL table
        df.to_sql(table_name, engine, if_exists='replace', index= False)
        print(f"Data uploaded successfully to the table '{table_name}' in the database.")

# This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
# The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.
class DataExtractor():
    #This method is to set the initial state of the object
    def __init__(self, headers=None):
        self.headers = headers

    # This method will extract the database table to a pandas DataFrame.    
    @staticmethod
    def read_rds_table(db_connector, file_path, table_name, columns=None):
        engine = db_connector.init_db_engine(file_path)
        # Use a list of columns if specified, otherwise, select all columns
        columns_list = columns if columns else ['*']
        # Construct the query with specific columns
        query = f"SELECT {', '.join(columns_list)} FROM {table_name}"
        df = pd.read_sql_query(query, engine)
        return df
    
    # This method takes pdf link as an argument and returns a pandas DataFrame
    @staticmethod
    def retrieve_pdf_data(pdf_link):
        # Use tabula to extract tables from the PDF
        tables = tabula.read_pdf(pdf_link, pages='all', multiple_tables=True)

        # Concatenate all tables into a single DataFrame
        extracted_data = pd.concat(tables, ignore_index=True)

        return extracted_data

    # This method returns the number of stores to extract
    def list_number_of_stores(self, number_stores_endpoint):
            response = requests.get(number_stores_endpoint, headers=self.headers)
            data = response.json()
            # Check if the key 'number_of_stores' is present in the dictionary
            if 'number_stores' in data:
                return data['number_stores']
            else:
                print("Error: 'number_of_stores' key not found in API response.")
                return None

    # This method extracts all the stores from the API, saving them in a pandas DataFrame  
    def retrieve_stores_data(self, store_endpoint, number_of_stores):
        all_stores_data = []

        for store_number in range(0, number_of_stores):
            full_store_endpoint = store_endpoint.format(store_number=store_number)
            response = requests.get(full_store_endpoint, headers=self.headers)

            if response.status_code == 200:
                store_data = response.json()
                all_stores_data.append(store_data)
            else:
                print(f"Error retrieving data for store {store_number}. Status code: {response.status_code}")

        # Convert the list of dictionaries to a DataFrame
        stores_df = pd.DataFrame(all_stores_data)

        return stores_df
    
    # This method uses the boto3 package to download and extract the information returning a pandas DataFrame
    @staticmethod
    def extract_from_s3(s3_address, file_format='csv'):
    # Initialize the S3 client
        s3_client = boto3.client('s3')

    # Extract bucket name and object key from the S3 address
        bucket_name, object_key = s3_address.replace('s3://', '').split('/', 1)

        try:
        # Download the file from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read()

        # Convert bytes to a pandas DataFrame based on the specified file format
            if file_format.lower() == 'csv':
                df = pd.read_csv(BytesIO(content))
            elif file_format.lower() == 'json':
                df = pd.read_json(BytesIO(content))
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

        # Return the DataFrame
            return df

        except Exception as e:
             print(f"Error extracting data from S3: {e}")
        return None

# You will use this class to clean data from each of the data sources.
class DataCleaning:
    # This method will perform the cleaning of the user data.
    @staticmethod
    def clean_user_data(user_data_df):
        # Creates a copy to avoid modifying the original DataFrame
        cleaned_user_data_df = user_data_df.copy()
        # Handling NULL values
        cleaned_user_data_df.dropna(inplace=True)

        # Checking for errors with dates and formatting
        cleaned_user_data_df['date_of_birth'] = pd.to_datetime(cleaned_user_data_df['date_of_birth'], errors='coerce')
        cleaned_user_data_df['join_date'] = pd.to_datetime(cleaned_user_data_df['join_date'], errors='coerce')
        
        # Handling incorrectly typed values (if any)
        # Converting columns to appropriate data types
        cleaned_user_data_df['country_code'] = cleaned_user_data_df['country_code'].astype(str)
        cleaned_user_data_df['phone_number'] = cleaned_user_data_df['phone_number'].astype(str)
        
        # Checking for rows filled with wrong information 
        # Removing rows with invalid dates
        current_date = datetime.now()
        oldest_reasonable_age = 120  # Assuming the oldest age considered reasonable
        cleaned_user_data_df = cleaned_user_data_df[
            (cleaned_user_data_df['date_of_birth'] < current_date) & 
            (cleaned_user_data_df['date_of_birth'] > (current_date - pd.DateOffset(years=oldest_reasonable_age)))
        ]
        
        return cleaned_user_data_df
    
    # Uses the following method to clean the data to remove any erroneous values, NULL values or errors with formatting.
    def clean_card_data(self, data):
        # Remove rows with NULL values
        cleaned_data = data.dropna()

        return cleaned_data
    
    # This method cleans the data retrieve from the API and returns a pandas DataFrame.
    @staticmethod
    def clean_store_data(store_data):
        # Creates a copy to avoid modifying the original list of dictionaries
        cleaned_store_data = store_data.copy()

        # Convert 'opening_date' to datetime and handle NULL values
        cleaned_store_data = pd.DataFrame(cleaned_store_data)
        cleaned_store_data['opening_date'] = pd.to_datetime(cleaned_store_data['opening_date'], errors='coerce')

        # Remove rows with NULL values in critical columns
        cleaned_store_data.dropna(subset=['store_code', 'continent'], inplace=True)

        # Convert columns to appropriate data types
        cleaned_store_data['store_code'] = cleaned_store_data['store_code'].astype(str)
        cleaned_store_data['lcontinent'] = cleaned_store_data['continent'].astype(str)

        return cleaned_store_data

    # This will take the products DataFrame as an argument and return the products DataFrame.
    @staticmethod
    def convert_product_weights(products_df):
        if 'weight' not in products_df.columns:
            print("Error: 'weight' column not found in the DataFrame.")
            return None

        # Directly access the 'weight' column values
        for index in range(len(products_df)):
            value = products_df.at[index, 'weight']

            # Convert ml to g using a 1:1 ratio
            if 'ml' in str(value):  
                weight_in_g = float(str(value).replace('ml', ''))  
                weight_in_kg = weight_in_g / 1000  
                products_df.at[index, 'weight'] = weight_in_kg
            else:
                pass

        return products_df

    # This method will clean the DataFrame of any additional erroneous values.
    @staticmethod
    def clean_products_data(products_df):

        # Removes rows with missing values in specific columns
        products_df = products_df.dropna(subset=['product_name'])

        # Removes duplicate rows
        products_df = products_df.drop_duplicates()

        return products_df
    
    # This method will clean the orders table data.Removes the columns, first_name, last_name and 1 to have the table in the correct form before uploading to the database.
    @staticmethod
    def clean_orders_data(orders_data_df):
        # Create a copy to avoid modifying the original DataFrame
        cleaned_orders_data_df = orders_data_df.copy()

        # Remove specified columns (first_name, last_name, and 1)
        columns_list = ['first_name', 'last_name', '1']
        cleaned_orders_data_df = cleaned_orders_data_df.drop(columns=columns_list, errors='ignore')

        return cleaned_orders_data_df
    
    # This method performs necessary cleaning for extracted data frame
    @staticmethod
    def date_events_table(date_events_table_df):
        # Drops rows with missing values
        cleaned_df = date_events_table_df.dropna()

        # Removes duplicates
        cleaned_df = cleaned_df.drop_duplicates()

        # Converts 'time_period' to uppercase
        cleaned_df['time_period'] = cleaned_df['time_period'].str.upper()

        # Drops 'date_uuid' column if not needed for further analysis
        #cleaned_df = cleaned_df.drop(columns=['date_uuid'])

        return cleaned_df

# Instantiate DatabaseConnector class
db_connector = DatabaseConnector()
# Instantiates DataExtractor class
db_extractor = DataExtractor()
# # Instantiates DataCleaning class
db_cleaning = DataCleaning()

# Provides the path to db_creds.yaml file
file_path = '/Users/emiltonsoosaippillai/desktop/multinational-retail-data-centralisation/db_creds.yaml'

# Provides the path to Local_database.yaml file
file_path_upload = '/Users/emiltonsoosaippillai/desktop/sales_data_copy_path.yaml'

# Reads user data table into a pandas DataFrame
user_data_df = db_extractor.read_rds_table(db_connector, file_path, "legacy_users" )
#cleaned_user_data_df = db_cleaning.clean_user_data(user_data_df.copy())
db_connector.upload_to_db(file_path_upload, user_data_df, 'dim_users')

# Displays the extracted user data DataFrame
print(user_data_df)

pdf_link = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
extracted_pdf_data = db_extractor.retrieve_pdf_data(pdf_link)
# Displays the extracted card details data DataFrame
print(extracted_pdf_data)

#cleaned_card_data = db_cleaning.clean_card_data(extracted_pdf_data)
# Displays the cleaned card details data DataFrame
#print(extracted_pdf_data)

db_connector.upload_to_db(file_path_upload, extracted_pdf_data, 'dim_card_details')

headers = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
store_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'
number_stores_endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'

store_data_extractor = DataExtractor(headers=headers)
# Get the number of stores
number_of_stores = store_data_extractor.list_number_of_stores(number_stores_endpoint)
print(f"Number of stores to extract: {number_of_stores}")

# Retrieve details for each store and save them in a DataFrame
if number_of_stores is not None:
    stores_df = store_data_extractor.retrieve_stores_data(store_endpoint, number_of_stores)
    print("Details for all stores:")
    print(stores_df)
    
# Clean the store data
#cleaned_stores_df = db_cleaning.clean_store_data(stores_df)
#print("Details for all stores:")
#print(stores_df)
# Upload cleaned store data to the database
db_connector.upload_to_db(file_path_upload, stores_df, 'dim_store_details')


s3_address = 's3://data-handling-public/products.csv'
products_df = db_extractor.extract_from_s3(s3_address)
# Display the extracted DataFrame
print("Products Dataframe")
print(products_df)

# Converts product weights
#cleaned_products_df = db_cleaning.convert_product_weights(products_df)

# Cleans products data
#final_cleaned_df = db_cleaning.clean_products_data(products_df)
# Displays the final cleaned Data
#print("Final Cleaned Products Data")
#print(final_cleaned_df)
# Uploads final cleaned products data to the database
db_connector.upload_to_db(file_path_upload, products_df, 'dim_products')


# Uses the read_rds_table method to extract orders data
orders_data_df = db_extractor.read_rds_table(db_connector,file_path, "orders_table")

# Displays the extracted orders data DataFrame
print("Orders_table Data:")
print(orders_data_df)

# Cleans the orders data
#cleaned_orders_data_df = db_cleaning.clean_orders_data(orders_data_df)

# Displays the cleaned orders data DataFrame
#print("Cleaned Orders Data:")
#print(orders_data_df)

# Uploads Final cleaned orders data to the database
db_connector.upload_to_db(file_path_upload, orders_data_df, 'orders_table')

# Extracts data from the JSON file on S3
s3_date_details_address = 's3://data-handling-public/date_details.json'
date_details_df = db_extractor.extract_from_s3(s3_date_details_address,file_format='json')

# Displays the extracted DataFrame
print("Date Details Data")
print(date_details_df)

# Cleans the table
#cleaned_date_events_table_df = DataCleaning.date_events_table(date_details_df)

# Displays the cleaned DataFrame
#print("Cleaned date events table Data:")
#print(date_details_df)

# Upload cleaned date events details data to the database
db_connector.upload_to_db(file_path_upload, date_details_df, 'dim_date_times')
