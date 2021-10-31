from downloader import download, load_company_value
from utils import json_loads, load_ua

if __name__ == '__main__':
    print(load_company_value(update=False))
