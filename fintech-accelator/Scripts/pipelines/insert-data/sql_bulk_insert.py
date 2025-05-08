import re
import sys
import argparse
from pathlib import Path
import os
from tqdm import tqdm


def parse_insert_line(line):
    """Extract values from an INSERT line"""
    match = re.search(r"VALUES\s*\((.*)\);", line.strip(), re.IGNORECASE)
    return match.group(1) if match else None


def create_directory_if_not_exists(directory_path):
    """Create directory if it doesn't exist"""
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def get_table_info(line):
    """Extract table name and columns from an INSERT line"""
    match = re.match(r"INSERT INTO (\S+)\s*\((.*?)\)\s*VALUES", line, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)
    return None, None


def generate_bulk_insert_file(table_name, columns, values_list, output_path, batch_size):
    """Generate bulk INSERT file with batched statements"""
    total_batches = (len(values_list) + batch_size - 1) // batch_size
    
    with open(output_path, 'w', encoding='utf-8') as out:
        for i in tqdm(range(0, len(values_list), batch_size), 
                      desc=f"Generating batches for {output_path.name}",
                      total=total_batches):
            batch = values_list[i:i+batch_size]
            out.write("BEGIN;\n")
            out.write(f"INSERT INTO {table_name} ({columns}) VALUES\n")
            out.write(",\n".join(f"({v})" for v in batch))
            out.write(";\nCOMMIT;\n\n")
    
    print(f"✅ Script generated successfully: {output_path}")


def convert_to_bulk_insert(batch_size):
    """Convert SQL files with individual INSERTs to batched INSERTs"""
    # Base path for SQL files
    base_path = Path("../../../data/sql")
    
    # Output directory path
    output_dir = base_path / "Bulk-Load"
    create_directory_if_not_exists(output_dir)
    
    FILES_SQL = [
        #'04-FINTECH-CLIENTS.sql',
        #'05-FINTECH-ISSUERS.sql',
        #'06-FINTECH-FRANCHISES.sql',
        #'07-FINTECH-MERCHANT_LOCATIONS.sql',
        #'08-FINTECH-CREDIT_CARDS.sql',
        #'09-FINTECH-TRANSACTIONS.sql'
    ]
    
    print("Starting SQL files processing...")
    for file_name in tqdm(FILES_SQL, desc="Processing SQL files"):
        file_path = base_path / file_name
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            continue

        table_name = None
        columns = None
        values_list = []

        # Count total lines for progress bar
        total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in tqdm(f, total=total_lines, desc=f"Reading {file_name}", leave=False):
                line = line.strip()
                if not line or not line.lower().startswith("insert into"):
                    continue

                if table_name is None:
                    table_name, columns = get_table_info(line)
                    if not table_name or not columns:
                        print(f"⚠️ Could not extract table information from {file_name}")
                        break

                values = parse_insert_line(line)
                if values:
                    values_list.append(values)

        if not values_list:
            print(f"⚠️ No values found to insert in {file_name}")
            continue

        # Create output file with the same name but in the Bulk-Load folder
        output_file = output_dir / f"{file_name[:-4]}_bulk_batches.sql"
        generate_bulk_insert_file(table_name, columns, values_list, output_file, batch_size)


def main():
    parser = argparse.ArgumentParser(
        description="Convert individual INSERTs to batched INSERTs with BEGIN/COMMIT."
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=10000, 
        help="Batch size for INSERT statements (default: 10000)"
    )

    args = parser.parse_args()
    convert_to_bulk_insert(args.batch_size)


if __name__ == "__main__":
    main()