#!/usr/bin/env python3
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake_data_generic import FakeGenericTable
from read_columns_from_file import read_column_data

 # Card Franquises
CARD_NETWORKS = [
        "Visa",
        "MasterCard",
        "American Express",
        "Discover",
        "UnionPay",
        "JCB",
        "Diners Club",
        "RuPay",
        "Troy",
        "Verve",
        "Interac",
        "BC Card",
        "Mir",
        "Elo",
        "Maestro",
        "Cirrus",
        "STAR",
        "Accel",
        "PULSE",
        "Visa Electron"
    ]

def generate_data_dummy(auto_prefix:str = None):
    """
    Example of generating data for the FRANCHISES table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.FRANCHISES (
        franchise_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        issuer_id VARCHAR(50) NOT NULL,
        country_code VARCHAR(3) NOT NULL
    );

    """
    # Define columns in order
    columns = [
        'name',
        'issuer_id',
        'country_code'
    ]
    # Define faker providers for each
    
    
    faker_providers = [
        # name
        lambda faker: random.choice(CARD_NETWORKS),
        # issuer_id
        'random_value',
        # country_code
        'random_value'
    ]
    
    # Add foreign keys
    foreign_keys = {
        
        'issuer_id': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-ISSUERS.txt',
            column_number = 1),
        
        'country_code': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-COUNTRIES.txt',
            column_number = 1)  # Placeholder - will be populated with real client_ids
    }
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='franchises',
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