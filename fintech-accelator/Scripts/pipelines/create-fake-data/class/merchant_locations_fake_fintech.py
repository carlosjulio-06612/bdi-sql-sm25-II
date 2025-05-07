#!/usr/bin/env python3
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fake_data_generic import FakeGenericTable
from read_columns_from_file import read_column_data

def generate_data_dummy(auto_prefix:str = None):
    """
    Example of generating data for the MERCHANT_LOCATIONS table.
    
    Table definition:
    CREATE TABLE IF NOT EXISTS fintech.MERCHANT_LOCATIONS (
        location_id SERIAL PRIMARY KEY,
        store_name VARCHAR(100) NOT NULL,
        category VARCHAR(100) NOT NULL,
        city VARCHAR(100) NOT NULL,
        country_code VARCHAR(3) NOT NULL,
        latitude DECIMAL(10,6),
        longitude DECIMAL(10,6)
    );

    """
    # Define columns in order
    columns = [
        'store_name',
        'category',
        'city',
        'country_code',
        'latitude',
        'longitude'
    ]
    # Custom Categories and Adjectives
    ADJECTIVES = ["Happy", "Green", "Modern", "Sunny", "Golden", "Urban"]
    CATEGORIES =  ['Market', 'Shop', 'Boutique', 'Emporium', 'Outlet', 'Store', 'Depot', 'Mart', 'Bazaar', 'Trading Co.', 'Supply', 'Warehouse', 'Corner', 'Cart', 'Stand', 'Kiosk', 'Studio', 'Gallery', 'Collection', 'General Store']
    NOUNS = ['Heavy', 'Page', 'Political', 'Activity', 'Somebody', 'Try', 'Friend', 'Imagine', 'Shoulder', 'Drive', 'He', 'Range', 'Challenge', 'Station', 'Treatment', 'Its', 'Attack', 'Affect', 'Girl', 'Marriage']
    
    # Define faker providers for each column
    
    faker_providers = [
        # 'store_name'
        lambda _: random.choice(ADJECTIVES) + " " + random.choice(NOUNS) + " " + random.choice(CATEGORIES),
        
        # 'category'
        lambda _: random.choice(CATEGORIES),
        
        # 'city'
        'city',
        
        # 'country_code'
        'random_value',
        
        # 'latitude'
        lambda faker: faker.latitude(),
        
        # 'longitude'
        lambda faker: faker.longitude()
    ]
    
    # Add foreign keys
    foreign_keys = {
        'country_code': read_column_data(
            file_path = '../../../data/sql/FK-Values/FK-FINTECH-COUNTRIES.txt',
            column_number = 1)  # Placeholder - will be populated with real client_ids
    }
    
    # Create the table
    data_table = FakeGenericTable(
        table_name='merchant_locations',
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
    parser.add_argument('--prefix', type=str, default='XX', help='prefix of file')
    
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