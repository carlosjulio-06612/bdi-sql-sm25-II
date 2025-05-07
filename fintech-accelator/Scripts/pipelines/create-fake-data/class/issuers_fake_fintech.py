#!/usr/bin/env python3
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake_data_generic import FakeGenericTable
from read_columns_from_file import read_column_data

def generate_data_dummy(auto_prefix:str = None):
    """
    Example of generating data for the ISSUERS table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.ISSUERS (
        issuer_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        bank_code VARCHAR(50) NOT NULL,
        contact_phone VARCHAR(50),
        international BOOLEAN DEFAULT FALSE,
        country_code VARCHAR(10) NOT NULL
    );

    """
    # Define columns in order
    columns = [
        'issuer_id',
        'name',
        'bank_code',
        'contact_phone',
        'international',
        'country_code'
    ]
    
    # Groups Bank
    BANKS_SUFFIX = [
        'Corp',
        'Bank',
        'Associate',
        'Rental',
        'Private Bank',
        'Public Bank'
    ]
    # Define faker providers for each column
    faker_providers = [
        # issuer_id
        lambda faker: f"ISU-{faker.random_number(digits=25)}",
        # name
        lambda faker: faker.company()[:-5] + random.choice(BANKS_SUFFIX),
        # bank code (50% probability foreach one)
        lambda faker: random.choice([faker.iban, faker.bban])(),
        # contact_phone
        lambda faker: faker.country_calling_code() + faker.msisdn()[:-5],
        # international
        lambda _: 'TRUE' if random.random() < 0.85 else 'FALSE',
        # country_code
        'random_element'
    ]
    
    # Add foreign keys
    foreign_keys = {
        'country_code': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-COUNTRIES.txt',
            column_number = 1)  # Placeholder - will be populated with real client_ids
    }
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='issuers',
        schema_name='fintech',
        columns=columns,
        path_output='../../../data/sql',
        prefix=auto_prefix,
        faker_providers=faker_providers,
        foreign_keys=foreign_keys
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
    # Export Foreign Keys Records
    dummy_table.export_foreign_keys_file(records, ['issuer_id'])