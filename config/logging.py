import logging
import os
import sys

def setup_logging(log_name = "scraping.log", level = logging.INFO):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(".")

    log_path = os.path.join(base_dir, log_name)

    logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    