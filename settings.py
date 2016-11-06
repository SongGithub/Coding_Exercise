import sys, os

BASE_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

INPUT_PATH = os.path.join(CONFIG_DIR, 'input.csv')
RESULT_DIR = os.path.join(BASE_DIR, 'result')
TAX_RATE_BACKUP_PATH = os.path.join(CONFIG_DIR, 'tax_rate_default.json')
