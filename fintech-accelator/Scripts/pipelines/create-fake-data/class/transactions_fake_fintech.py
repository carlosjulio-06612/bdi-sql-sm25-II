#!/usr/bin/env python3
import sys
import os
import random
from datetime import timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake_data_generic import FakeGenericTable
from read_columns_from_file import read_column_data

def generate_data_dummy(auto_prefix:str = None, records:int = None):
    """
    Example of generating data for the TRANSACTIONS table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.TRANSACTIONS (
        transaction_id VARCHAR(50) PRIMARY KEY,
        card_id VARCHAR(50) NOT NULL,
        amount DECIMAL(15,2) NOT NULL,
        currency VARCHAR(3) NOT NULL,
        transaction_date TIMESTAMP NOT NULL,
        channel VARCHAR(50) NOT NULL,
        status VARCHAR(20) NOT NULL,
        device_type VARCHAR(50),
        location_id INT NOT NULL,
        method_id INT NOT NULL
    );

    """
    # Define columns in order
    columns = [
        'transaction_id',
        'card_id',
        'amount',
        'currency',
        'transaction_date',
        'channel',
        'status',
        'device_type',
        'location_id',
        'method_id'
    ]
    
    # Transaction status
    TRANSACTION_STATUS = ["Completed", "Rejected", "Pending"]

    # Extended list of device types
    DEVICE_TYPES = [
        "POS",             # Point of Sale terminal
        "mobile",          # Mobile app
        "Web browser",     # Desktop or mobile browser
        "Tablet",          # Tablet device
        "Smartwatch",      # Wearable device
        "Kiosk",           # Self-service terminal
        "Voice assistant", # Voice-based transaction (e.g., Alexa, Google Assistant)
        "ATM",             # Automated Teller Machine
        "Smart TV",        # Rare, but possible for purchases
        "Car system"       # In-car systems (e.g., Tesla screen)
    ]
    # Channel used
    CHANNEL = ['Physical', 'Digital']

   
    # Define faker providers for each column
    faker_providers = [
        # transaction id
        lambda faker: f"TS-{faker.random_number(digits=25)}{random.choice(['AM','PM'])}",
        # card_id
        'random_value',
        # amount
        lambda faker: faker.pydecimal(left_digits=13, right_digits=2, positive=True),
        # currency
        'random_value',
        # transaction_date
        lambda faker: faker.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
        # channel
        lambda faker: random.choice(CHANNEL),
        # status
        lambda faker: random.choice(TRANSACTION_STATUS),
        # device type
        lambda faker: random.choice(DEVICE_TYPES),
        # location_id
        'random_value',
        # method_id
        'random_value'
    ]
    
    # Add foreign keys
    foreign_keys = {
        
        'card_id': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-CREDIT_CARDS.txt',
            column_number = 1),
        'currency': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-COUNTRIES.txt',
            column_number = 2),
        'location_id': [id for id in range(1, (records + 1))],
        'method_id': [id for id in range(1, (4 + 1))],
        
    }
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='transactions',
        schema_name='fintech',
        columns=columns,
        path_output='../../../data/sql',
        faker_providers=faker_providers,
        prefix=auto_prefix,
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
    dummy_table = generate_data_dummy(args.prefix, args.records)
    
    # Generate fake data
    records = dummy_table.generate_fake_data(
        num_records=args.records,
        seed=args.seed,
        variability=args.variability
    )
    
    # Export to SQL file
    dummy_table.export_to_sql_file(records)