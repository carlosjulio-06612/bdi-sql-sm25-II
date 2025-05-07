#!/usr/bin/env python3
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fake_data_generic import FakeGenericTable

def generate_data_dummy(auto_prefix:str = None):
    """
    Example of generating data for the CLIENTS table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.CLIENTS (
        client_id VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        middle_name VARCHAR(100),
        last_name VARCHAR(100) NOT NULL,
        gender VARCHAR(10),
        birth_date DATE,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(50),
        address VARCHAR(255)
    );
    """
    # Define columns in order
    columns = [
        'client_id',
        'first_name',
        'middle_name',
        'last_name',
        'gender',
        'birth_date',
        'email',
        'phone',
        'address'
    ]
    
    # define custom domains
    CUSTOM_DOMAINS = [
            "gmail.com",      
            "yahoo.com",      
            "outlook.com",    
            "example.com",    
            "fintechmail.com",
            "myapp.io",       
            "securemail.net", 
            "datahub.org",    
            "mailpro.tech",   
            "clientzone.co"   
    ]
    
    # Define faker providers for each column
    faker_providers = [
        # client_id: Custom format "CL-NNNNNN"
        lambda faker: f"CL-{faker.random_number(digits=15)}",
        
        # first_name: Use Faker's first_name method
        'first_name',
        
        # middle_name: Optional first name (70% chance of having one)
        lambda faker: faker.first_name() if faker.boolean(chance_of_getting_true=70) else None,
        
        # last_name: Use Faker's last_name method
        'last_name',
        
        # gender: Random selection from specific values
        {'method': 'random_element', 'elements': ('Male', 'Female', 'Other')},
        
        # birth_date: Birth date for an adult
        lambda faker: faker.date_of_birth(minimum_age=18, maximum_age=75).strftime('%Y-%m-%d'),
        
        # email: Custom email using first and last name

        lambda faker: faker.email().split('@')[0] + faker.last_name() + str(faker.random_number(digits=2)) + '@' + random.choice(CUSTOM_DOMAINS),
        
        # phone: Faker's phone_number method
        'phone_number',
        
        # address: Formatted address
        lambda faker: faker.address().replace('\n', ', ')
    ]
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='clients',
        schema_name='fintech',
        columns=columns,
        path_output='../../../data/sql',
        prefix=auto_prefix,
        faker_providers=faker_providers
    )
    
    return data_table


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate fake data for the CLIENTS table')
    parser.add_argument('--records', type=int, required=True, help='Number of records to generate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--variability', type=float, default=0.3, 
                       help='Locale variability (0-1, where 0 = single locale, 1 = all locales)')
    parser.add_argument('--prefix', type=str, default='XX', 
                       help='prefix of file')
    
    args = parser.parse_args()
    
    # Create table
    dummy_table = generate_data_dummy(args.prefix)
    
    # Generate fake data
    records = dummy_table.generate_fake_data(
        num_records=args.records,
        seed=args.seed,
        variability=args.variability
    )
    
    # Export to SQL file
    dummy_table.export_to_sql_file(records)
    # Export column client_id
    dummy_table.export_foreign_keys_file(records, ['client_id'])