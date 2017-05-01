"""
This file holds environmental variables for the project
"""
import sys, os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOURCE_DIR = os.path.join(BASE_DIR,'src')
CONFIG_DIR = os.path.join(SOURCE_DIR, 'config')
TEST_DIR =os.path.join(BASE_DIR,'tests')
TEST_FIXTURE_DIR = os.path.join(TEST_DIR,'fixtures')


INPUT_PATH = os.path.join(CONFIG_DIR, 'input.csv')
RESULT_DIR = os.path.join(SOURCE_DIR, 'result')

TAX_RATE_BACKUP_PATH = os.path.join(CONFIG_DIR, 'tax_rate_backup')
TAX_RATE_DEFAULT_FILENAME = 'tax_rate_default.json'
TAX_RATE_FINANCIAL_YEAR = "2015-16"