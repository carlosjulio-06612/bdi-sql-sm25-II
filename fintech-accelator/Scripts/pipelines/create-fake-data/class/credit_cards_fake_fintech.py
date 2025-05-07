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
    Example of generating data for the CREDIT_CARDS table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.CREDIT_CARDS (
        card_id VARCHAR(50) PRIMARY KEY,
        client_id VARCHAR(50) NOT NULL,
        issue_date DATE NOT NULL,
        expiration_date DATE NOT NULL,
        status VARCHAR(20) NOT NULL,
        franchise_id INT NOT NULL
    );

    """
    # Define columns in order
    columns = [
        'card_id',
        'client_id',
        'issue_date',
        'expiration_date',
        'status',
        'franchise_id'
    ]
    
    # Groups Bank
    STATUS = [
        'Activate',
        'Blocked',
        'Canceled',
    ]
   
    # Define faker providers for each column
    faker_providers = [
        # card_id
        lambda faker: faker.credit_card_number(),
        # client_id
        'random_value',
        # issue_date
        lambda faker: faker.date_between(start_date='-5y', end_date='-1y'),
        # expiration_date
        lambda faker: (faker.date_between(start_date='-5y', end_date='-1y') + timedelta(days=365 * random.randint(3, 5))).strftime('%Y-%m-%d'),
        # status
         lambda faker: random.choice(STATUS),
        # franchise_id
        'random_value'
    ]
    
    # Add foreign keys
    foreign_keys = {
        
        'client_id': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-CLIENTS.txt',
            column_number = 1),  # Placeholder - will be populated with real client_ids
        'franchise_id': [id for id in range(1, (records + 1))]
    }
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='credit_cards',
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
    dummy_table = generate_data_dummy(args.prefix, args.records)
    
    # Generate fake data
    records = dummy_table.generate_fake_data(
        num_records=args.records,
        seed=args.seed,
        variability=args.variability
    )
    
    # Export to SQL file
    dummy_table.export_to_sql_file(records)
    # Export Foreign Keys Records
    dummy_table.export_foreign_keys_file(records, ['card_id'])