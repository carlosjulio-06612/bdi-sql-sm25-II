import os
import time
import logging
from tqdm import tqdm
import argparse
from datetime import datetime

# Fixed list of scripts to execute
SCRIPT_LIST = [
    'clients_fake_fintech.py',
    'issuers_fake_fintech.py',
    'franchises_fake_fintech.py',
    'merchant_locations_fake_fintech.py',
    'credit_cards_fake_fintech.py',
    'transactions_fake_fintech.py'
]

def setup_logging():
    """Configure the logging format to match your example"""
    logger = logging.getLogger('script_runner')
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler('script_execution.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def check_virtual_environment():
    """Check if virtual environment is activated"""
    if not os.environ.get('VIRTUAL_ENV'):
        logger.error("Virtual environment not activated. Please activate it first.")
        return False
    return True

def execute_scripts(records, variability, start_prefix=3):
    """Execute all scripts sequentially with proper logging"""
    logger = setup_logging()
    
    if not check_virtual_environment():
        return
    
    logger.info(f"Starting execution of {len(SCRIPT_LIST)} scripts")
    logger.info(f"Parameters - records: {records}, variability: {variability}, start_prefix: {start_prefix}")
    
    try:
        with tqdm(total=len(SCRIPT_LIST), desc="Processing scripts") as pbar:
            for i, script_name in enumerate(SCRIPT_LIST):
                current_prefix = start_prefix + i
                prefix = f"{current_prefix:02d}"
                
                cmd = (
                    f"python .\\class\\{script_name} "
                    f"--records {records} "
                    f"--variability {variability} "
                    f"--prefix {prefix}"
                )
                
                logger.info(f"Executing script: {script_name}")
                logger.info(f"Using prefix: {prefix}")
                logger.debug(f"Full command: {cmd}")
                
                start_time = time.time()
                exit_code = os.system(cmd)
                execution_time = time.time() - start_time
                
                if exit_code != 0:
                    logger.error(f"Script failed with exit code: {exit_code}")
                    logger.error(f"Execution time: {execution_time:.2f}s")
                    break
                
                logger.info(f"Successfully executed: {script_name}")
                logger.info(f"Execution time: {execution_time:.2f}s")
                pbar.update(1)
                
                if i < len(SCRIPT_LIST) - 1:
                    time.sleep(1)
        
        logger.info("All scripts executed successfully")
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute fintech scripts sequentially')
    parser.add_argument('--records', type=int, default=10,
                      help='Number of records to generate (default: 10)')
    parser.add_argument('--variability', type=float, default=0.25,
                      help='Variability parameter (default: 0.25)')
    parser.add_argument('--start_prefix', type=int, default=3,
                      help='Starting prefix number (default: 3)')
    
    args = parser.parse_args()
    
    logger = setup_logging()
    execute_scripts(
        records=args.records,
        variability=args.variability,
        start_prefix=args.start_prefix
    )