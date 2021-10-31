from utils import load_headers

import requests
from lxml import etree
import json


def download(url, headers):
    req = requests.get(url, headers=headers)
    return req


def load_company_value(url='https://www.1point3acres.com/bbs/forum-198-1.html', update=True):
    if update:
        headers = load_headers('desktop', 'mac', 'chrome')
        req = download(url, headers)
        content = etree.HTML(req.text)
        company_list = content.xpath('//*[@id="company"]//option')
        res_dict = {}
        for company in company_list:
            value = int(company.xpath('./@value')[0])
            key = company.text
            if value > 0 and key:
                res_dict[key] = value
        js = json.dumps(res_dict)
        with open('./selective_key_value.json', 'w') as f:
            f.write(js)
        return res_dict
    else:
        with open('./selective_key_value.json') as f:
            res_dict = json.load(f)
        return res_dict
