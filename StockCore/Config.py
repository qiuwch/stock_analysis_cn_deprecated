import os

ROOT_DIR = os.path.pardir
DATA_DIR = os.path.join(ROOT_DIR, 'data/')
SZ_DATA_DIR = os.path.join(DATA_DIR, 'SZ/')
SHENZHEN_LIST = os.path.join(DATA_DIR, 'ShenzhenTradingHistoryIndex.txt') # company list
SHENZHEN_COMPANY_INFO = os.path.join(DATA_DIR, 'ShenzhenCompanyInfo.txt') # company information