import os
from typing import List

def read_column_data(file_path: str, column_number: int = 1, delimiter: str = '|', skip_header:bool = True) -> List[str]:
    """
    Flexible function that handles both single-column and delimited files
    
    Args:
        file_path: Path to the input file
        column_number: Column to extract (default: 1)
        delimiter: Column separator (None for single-column files)
        
    Returns:
        List of values from the specified column
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if not lines:
        raise ValueError("File is empty")
    
    # skip header
    if skip_header and len(lines) > 1:
        lines = lines[1:]
        
    # Single-column mode
    if delimiter is None:
        return lines
    
    # Multi-column mode
    result = []
    for i, line in enumerate(lines):
        parts = line.split(delimiter)
        if len(parts) < column_number:
            raise ValueError(f"Line {i+1} has only {len(parts)} columns")
        result.append(parts[column_number-1].strip())
    
    return result