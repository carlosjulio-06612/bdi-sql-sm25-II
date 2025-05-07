#!/usr/bin/env python3
import argparse
import math
import random
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple, Callable

from faker import Faker


class FakeGenericTable:
    """
    Generic table generator that accepts column definitions, faker providers, and schema.
    """
    
    # Available locales for data generation
    AVAILABLE_LOCALES = [
        'en_US', 'en_GB', 'en_AU', 'en_CA',
        'es_ES', 'es_MX', 'es_AR',
        'fr_FR', 'fr_CA',
        'it_IT',
        'pt_BR', 'pt_PT',
        'nl_NL', 'sv_SE', 'pl_PL', 'tr_TR',
        'cs_CZ', 'da_DK', 'fi_FI', 'no_NO',
        'ro_RO', 'hu_HU', 'sk_SK', 'sl_SI', 'hr_HR',
        'et_EE', 'lv_LV', 'lt_LT'
    ]

    def __init__(self, 
                 table_name: str,
                 schema_name: str,
                 columns: List[str],
                 faker_providers: List[Union[str, Dict, Callable]],
                 path_output: str = None,
                 prefix: str = None,
                 foreign_keys: Optional[Dict[str, List[Any]]] = None):
        """
        Initialize the generic table object.
        
        Args:
            table_name: Name of the table
            schema_name: Database schema name
            columns: List of column names in order
            faker_providers: List of faker provider methods or custom functions
                            Can be:
                            - String: name of a Faker method (e.g., 'name', 'email')
                            - Dict: {'method': 'random_element', 'elements': ['a', 'b', 'c']}
                            - Function: lambda faker: f"PREFIX-{faker.random_number()}"
            foreign_keys: Dictionary mapping foreign key columns to lists of valid values
                          e.g., {'country_id': [1, 2, 3]}
        """
        self.table_name = table_name
        self.schema_name = schema_name
        self.columns = columns
        self.faker_providers = faker_providers
        self.foreign_keys = foreign_keys or {}
        self.path_output = self._resolve_output_path(path_output)
        self.prefix = prefix
        
        # Validate that columns and faker_providers have the same length
        if len(columns) != len(faker_providers):
            raise ValueError(f"Number of columns ({len(columns)}) must match number of faker providers ({len(faker_providers)})")
    
    
    def _resolve_output_path(self, path_output: str = None) -> str:
        """
        Resolve the output directory path.
        
        Handles three cases:
        1. None -> uses default '../../data' relative to current file
        2. Relative path -> converts to absolute path
        3. Absolute path -> uses as-is
        
        Args:
            path_output: User-provided path or None
            
        Returns:
            Absolute path to output directory (created if didn't exist)
        """
        if path_output is None:
            # Default relative path: two levels up in 'data' folder
            default_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        else:
            default_path = path_output
        
        # Convert to absolute path and normalize (handles ../, ./ etc.)
        abs_path = os.path.abspath(default_path)
        
        # Create directory if it doesn't exist
        os.makedirs(abs_path, exist_ok=True)
        
        return abs_path
    
    def get_full_table_name(self) -> str:
        """
        Get the fully qualified table name with schema.
        
        Returns:
            Full table name in format schema_name.table_name
        """
        return f"{self.schema_name}.{self.table_name}"
    
    def _select_locales(self, variability: float) -> List[str]:
        """
        Select a subset of locales based on the variability parameter.
        
        Args:
            variability: Value between 0 and 1 determining how many locales to use
                         (0 = single locale, 1 = all locales)
        
        Returns:
            List of selected locale codes
        """
        if variability <= 0:
            return [self.AVAILABLE_LOCALES[0]]  # Default to en_US
        
        num_locales = math.ceil(variability * len(self.AVAILABLE_LOCALES))
        num_locales = max(1, min(num_locales, len(self.AVAILABLE_LOCALES)))
        
        return random.sample(self.AVAILABLE_LOCALES, num_locales)
    
    def _get_faker_for_locale(self, locale: str) -> Faker:
        """
        Create a Faker instance for a specific locale.
        
        Args:
            locale: Locale code (e.g., 'en_US')
            
        Returns:
            Faker instance configured with the specified locale
        """
        return Faker(locale)
    
    def _get_data_for_column(self, faker: Faker, column: str, provider_info: Union[str, Dict, Callable]) -> Any:
        """
        Generate fake data for a specific column based on its provider.
        
        Args:
            faker: Faker instance to use for data generation
            column: Column name
            provider_info: Provider specification (string, dict, or function)
            
        Returns:
            Generated data value
        """
        # First check if it's a foreign key
        if column in self.foreign_keys:
            # For foreign keys, randomly select a value from the provided list
            return random.choice(self.foreign_keys[column])
        
        # Handle different types of provider specifications
        if isinstance(provider_info, str):
            # Provider is a method name on the faker instance
            if not hasattr(faker, provider_info):
                raise ValueError(f"Unknown Faker provider: {provider_info}")
            
            faker_method = getattr(faker, provider_info)
            return faker_method()
            
        elif isinstance(provider_info, dict):
            # Provider is a dict with method and parameters
            if 'method' not in provider_info:
                raise ValueError(f"Provider dict must have a 'method' key: {provider_info}")
            
            method_name = provider_info['method']
            if not hasattr(faker, method_name):
                raise ValueError(f"Unknown Faker provider method: {method_name}")
            
            # Extract method parameters
            params = {k: v for k, v in provider_info.items() if k != 'method'}
            
            # Call the method with parameters
            faker_method = getattr(faker, method_name)
            return faker_method(**params)
            
        elif callable(provider_info):
            # Provider is a custom function
            return provider_info(faker)
            
        else:
            # Unknown provider type
            raise ValueError(f"Unsupported provider type for column {column}: {type(provider_info)}")
    
    def generate_fake_data(self, 
                          num_records: int, 
                          seed: int = 42, 
                          variability: float = 0.3) -> List[Dict[str, Any]]:
        """
        Generate fake data for the table.
        
        Args:
            num_records: Number of records to generate
            seed: Seed for random number generation to ensure reproducibility
            variability: Value between 0 and 1 determining locale variability
            
        Returns:
            List of dictionaries containing fake data for each record
        """
        random.seed(seed)
        Faker.seed(seed)
        
        # Select locales based on variability
        selected_locales = self._select_locales(variability)
        print(f"Using {len(selected_locales)} locales: {', '.join(selected_locales)}")
        
        # Create Faker instances for each locale
        faker_instances = [self._get_faker_for_locale(locale) for locale in selected_locales]
        
        records = []
        for i in range(num_records):
            # Select a random locale for this record
            faker = random.choice(faker_instances)
            
            record = {}
            for column, provider in zip(self.columns, self.faker_providers):
                record[column] = self._get_data_for_column(faker, column, provider)
            
            records.append(record)
        
        return records
    
    def _format_value_for_sql(self, value: Any) -> str:
        """
        Format a value for inclusion in an SQL INSERT statement.
        
        Args:
            value: The value to format
            
        Returns:
            String representation of the value suitable for SQL
        """
        if value is None:
            return 'NULL'
        elif isinstance(value, bool):
            return str(int(value))
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            # Escape single quotes in strings
            return str(value).replace("'", "''")
    
    def to_sql(self, records: List[Dict[str, Any]]) -> str:
        """
        Convert records to SQL INSERT statements.
        
        Args:
            records: List of record dictionaries
            
        Returns:
            String containing SQL INSERT statements
        """
        if not records:
            return ""
        
        sql_statements = []
        
        # Get column names from the first record
        columns = list(records[0].keys())
        columns_str = ', '.join(columns)
        
        # Use the fully qualified table name with schema
        full_table_name = self.get_full_table_name()
        
        for record in records:
            values = [self._format_value_for_sql(record[column]) for column in columns]
            values_str = ', '.join(values)
            
            sql = f"INSERT INTO {full_table_name} ({columns_str}) VALUES ({values_str});"
            sql_statements.append(sql)
        
        return '\n'.join(sql_statements)
    
    def export_to_sql_file(self, records: List[Dict[str, Any]]) -> None:
        """
        Export records to an SQL file in the configured output directory.
        
        Args:
            records: List of record dictionaries to export
        """
        filename = os.path.join(
            self.path_output,
            f"{self.prefix}-{self.schema_name.upper()}-{self.table_name.upper()}.sql"
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_sql(records))
        
        print(f"Exported {len(records)} records to {os.path.abspath(filename)}")
        
    def export_foreign_keys_file(self, records: List[Dict[str, Any]], columns_export: List[str]) -> None:
        """
        Export foreign keys records to a text file, creating directories if needed.

        Args:
            records: List of dictionaries containing the records
            columns_export: List of column names to export
        """
        # Validate input
        if not records or not columns_export:
            raise ValueError("Records and columns_export cannot be empty")
        
        # Verify columns exist
        sample_record = records[0]
        for col in columns_export:
            if col not in sample_record:
                raise KeyError(f"Column '{col}' not found in records")

        # Prepare file path
        output_dir = os.path.join(self.path_output, 'FK-Values')
        os.makedirs(output_dir, exist_ok=True)  # Create directory if doesn't exist
        
        output_file = os.path.join(
            output_dir,
            f"FK-{self.schema_name.upper()}-{self.table_name.upper()}.txt"
        )

        # Prepare content
        header = "|".join(columns_export)
        lines = [header] + [
            "|".join(str(record[col]) for col in columns_export)
            for record in records
        ]

        # Write file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
            print(f"✅ Successfully exported {len(records)} foreign keys to:\n{output_file}")
        except Exception as e:
            print(f"❌ Failed to export foreign keys: {str(e)}")
            raise
        


def main():
    """Parse command line arguments and generate fake data for the table."""
    parser = argparse.ArgumentParser(description='Generate fake data for database tables')
    parser.add_argument('--table', type=str, required=True, help='Table name')
    parser.add_argument('--schema', type=str, required=True, help='Database schema name')
    parser.add_argument('--columns', type=str, required=True, 
                       help='Comma-separated list of column names')
    parser.add_argument('--providers', type=str, required=True, 
                       help='Comma-separated list of Faker providers')
    parser.add_argument('--records', type=int, required=True, help='Number of records to generate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--variability', type=float, default=0.3, 
                        help='Locale variability (0-1, where 0 = single locale, 1 = all locales)')
    
    args = parser.parse_args()
    
    # Parse columns and providers
    columns = [col.strip() for col in args.columns.split(',')]
    providers = [provider.strip() for provider in args.providers.split(',')]
    
    # Create a Generic Table instance
    table = FakeGenericTable(
        table_name=args.table,
        schema_name=args.schema,
        columns=columns,
        faker_providers=providers
    )
    
    # Generate fake data
    records = table.generate_fake_data(
        num_records=args.records,
        seed=args.seed,
        variability=args.variability
    )
    
    # Export to SQL file
    table.export_to_sql_file(records)


if __name__ == "__main__":
    main()