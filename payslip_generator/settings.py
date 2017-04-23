"""
This file holds environmental variables for the project
"""

import sys, os

BASE_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

INPUT_PATH = os.path.join(CONFIG_DIR, 'input.csv')
RESULT_DIR = os.path.join(BASE_DIR, 'result')

TAX_RATE_BACKUP_PATH = os.path.join(CONFIG_DIR, 'tax_rate_backup')
TAX_RATE_DEFAULT_FILENAME = 'tax_rate_default.json'
TAX_RATE_FINANCIAL_YEAR = 1
TEMP_BUDGET_REPAIR_LEVY = [180000, 0.02]
